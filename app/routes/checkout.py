import uuid
import stripe
from flask import Blueprint, current_app, jsonify, request
from app import orders
from app.data import catalog_pricing, designer_pricing

bp = Blueprint("checkout", __name__, url_prefix="/api/checkout")


class CheckoutError(ValueError):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def _price_line(raw_line: dict, db_uri: str | None = None) -> dict:
    """
    Turns one client-submitted line into { name, image, quantity, unit_price, selections }.
    This is the only place prices are decided — raw_line.unitPrice (if the
    client even sent one) is never read.
    """
    product_id = raw_line.get("productId")
    quantity = raw_line.get("quantity")

    if not isinstance(quantity, int) or quantity < 1 or quantity > 20:
        raise CheckoutError(f"Invalid quantity for line: {quantity!r}")

    if product_id == "custom-pillow":
        config = raw_line.get("designerConfig") or {}
        try:
            unit_price = designer_pricing.compute_pillow_price(config)
            selections = designer_pricing.pillow_selection_summary(config)
        except (KeyError, designer_pricing.InvalidOptionError) as exc:
            raise CheckoutError(f"Invalid custom pillow configuration: {exc}") from exc
        name = "Custom Pillow"
        if config.get("monogram"):
            name += f" (monogram: {str(config['monogram'])[:3].upper()})"
        return {"name": name, "image": "/placeholder-pillow.svg", "quantity": quantity,
                "unit_price": unit_price, "selections": selections}

    if product_id == "custom-case":
        config = raw_line.get("designerConfig") or {}
        try:
            unit_price = designer_pricing.compute_case_price(config)
            selections = designer_pricing.case_selection_summary(config)
        except (KeyError, designer_pricing.InvalidOptionError) as exc:
            raise CheckoutError(f"Invalid custom pillowcase configuration: {exc}") from exc
        name = "Custom Pillowcase"
        if config.get("monogram"):
            name += f" (monogram: {str(config['monogram'])[:3].upper()})"
        return {"name": name, "image": "/placeholder-case.svg", "quantity": quantity,
                "unit_price": unit_price, "selections": selections}

    if not product_id:
        raise CheckoutError("Line is missing productId")

    selections = raw_line.get("selections") or {}
    try:
        priced = catalog_pricing.price_catalog_line(product_id, selections, db_uri=db_uri)
    except catalog_pricing.InvalidLineError as exc:
        raise CheckoutError(str(exc)) from exc

    product = priced["product"]
    return {
        "name": product["name"],
        "image": product["images"][0] if product.get("images") else "",
        "quantity": quantity,
        "unit_price": priced["unit_price"],
        "selections": priced["selection_summary"],
    }


def _db_uri() -> str:
    return current_app.config.get("DATABASE_URL") or current_app.config.get("DATABASE_PATH", "orders.db")


@bp.post("/session")
def create_session():
    stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]
    if not stripe.api_key:
        return jsonify({"error": "Payments aren't configured yet."}), 503

    body = request.get_json(silent=True) or {}
    raw_lines = body.get("lines")
    if not isinstance(raw_lines, list) or len(raw_lines) == 0:
        return jsonify({"error": "Your bag is empty."}), 400

    try:
        priced_lines = [_price_line(line, db_uri=_db_uri()) for line in raw_lines]
    except CheckoutError as exc:
        return jsonify({"error": str(exc)}), exc.status

    stripe_line_items = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {"name": line["name"]},
                "unit_amount": line["unit_price"],
            },
            "quantity": line["quantity"],
        }
        for line in priced_lines
    ]

    frontend_url = current_app.config["FRONTEND_URL"]

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=stripe_line_items,
            success_url=f"{frontend_url}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{frontend_url}/checkout/cancel",
            shipping_address_collection={"allowed_countries": ["US", "CA"]},
            automatic_tax={"enabled": True},
        )
    except stripe.error.StripeError as exc:
        return jsonify({"error": f"Stripe couldn't start checkout: {exc.user_message or str(exc)}"}), 502

    order_id = f"TD-{uuid.uuid4().hex[:8].upper()}"
    total = sum(line["unit_price"] * line["quantity"] for line in priced_lines)
    receipt_lines = [
        {"name": line["name"], "quantity": line["quantity"], "unitPrice": line["unit_price"]}
        for line in priced_lines
    ]
    orders.save_order(
        _db_uri(),
        session_id=session.id,
        order_id=order_id,
        email="",
        total=total,
        lines=receipt_lines,
    )

    return jsonify({"checkoutUrl": session.url})


@bp.post("/webhook")
def webhook():
    stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]
    payload = request.get_data()
    sig_header = request.headers.get("Stripe-Signature", "")
    webhook_secret = current_app.config["STRIPE_WEBHOOK_SECRET"]

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return jsonify({"error": "Invalid webhook signature"}), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        email = (session.get("customer_details") or {}).get("email", "")

        existing = orders.get_order_by_session_id(_db_uri(), session_id)
        if existing is not None:
            orders.save_order(
                _db_uri(),
                session_id=session_id,
                order_id=existing["orderId"],
                email=email,
                total=existing["total"],
                lines=existing["lines"],
            )

    return jsonify({"received": True})


@bp.get("/session/<session_id>")
def get_order(session_id: str):
    order = orders.get_order_by_session_id(_db_uri(), session_id)

    if order is not None and order["email"]:
        return jsonify(order)

    stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]
    try:
        session = stripe.checkout.Session.retrieve(session_id, expand=["line_items"])
    except stripe.error.StripeError:
        if order is not None:
            return jsonify(order)
        return jsonify({"error": "Order not found"}), 404

    if session.get("payment_status") != "paid":
        return jsonify({"error": "This order hasn't completed payment yet."}), 404

    email = (session.get("customer_details") or {}).get("email", "")
    line_items = session.get("line_items", {}).get("data", [])
    lines = [
        {
            "name": item["description"],
            "quantity": item["quantity"],
            "unitPrice": item["price"]["unit_amount"],
        }
        for item in line_items
    ]
    total = session.get("amount_total", 0)
    order_id = order["orderId"] if order else f"TD-{session_id[-8:].upper()}"

    orders.save_order(
        _db_uri(),
        session_id=session_id,
        order_id=order_id,
        email=email,
        total=total,
        lines=lines,
    )

    return jsonify({"orderId": order_id, "email": email, "total": total, "lines": lines})
