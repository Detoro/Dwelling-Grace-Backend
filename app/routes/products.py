from flask import Blueprint, abort, current_app, jsonify, request

from app import orders

bp = Blueprint("products", __name__, url_prefix="/api/products")


def _db_uri() -> str:
    return current_app.config.get("DATABASE_URL") or current_app.config.get("DATABASE_PATH", "orders.db")


def _parse_bool(value):
    if value is None:
        return None
    return value.lower() in ("true", "1", "yes")


@bp.get("")
def list_products():
    category = request.args.get("category")
    featured = _parse_bool(request.args.get("featured"))
    products = orders.get_all_products(_db_uri(), category=category, featured=featured)
    return jsonify(products)


@bp.get("/designer-options")
def get_designer_options():
    options = orders.get_designer_options(_db_uri())
    return jsonify(options)


@bp.get("/<slug>")
def get_product(slug: str):
    product = orders.get_product_by_slug(_db_uri(), slug)
    if product is None:
        abort(404, description=f"No product found for slug {slug!r}")
    return jsonify(product)
