from flask import Blueprint, current_app, jsonify, request

from app import orders

bp = Blueprint("newsletter", __name__, url_prefix="/api/newsletter")


def _db_uri() -> str:
    return current_app.config.get("DATABASE_URL") or current_app.config.get("DATABASE_PATH", "orders.db")


@bp.post("")
def subscribe():
    body = request.get_json(silent=True) or {}
    email = body.get("email")

    if not isinstance(email, str) or not email.strip() or "@" not in email or "." not in email:
        return jsonify({"error": "A valid email address is required."}), 400

    try:
        orders.subscribe_newsletter(_db_uri(), email.strip())
        return jsonify({"status": "subscribed", "email": email.strip().lower()}), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        current_app.logger.error(f"Newsletter subscription error: {exc}")
        return jsonify({"error": "Could not subscribe at this time. Please try again later."}), 500

