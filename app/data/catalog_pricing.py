from app.data import products as catalog
from app.orders import get_product_by_id

class InvalidLineError(ValueError):
    pass


def price_catalog_line(product_id: str, selections: dict, db_uri: str | None = None) -> dict:
    product = None
    if db_uri:
        product = get_product_by_id(db_uri, product_id)
    if product is None:
        product = catalog.find_by_id(product_id)
    if product is None:
        raise InvalidLineError(f"Unknown product id: {product_id!r}")

    price = product["basePrice"]
    summary = []

    for group in product.get("variantGroups", []):
        option_id = selections.get(group["id"])
        if option_id is None:
            if group.get("required"):
                raise InvalidLineError(f"Missing required selection: {group['id']!r}")
            continue
        option = next((o for o in group.get("options", []) if o["id"] == option_id), None)
        if option is None:
            raise InvalidLineError(f"Unknown option {option_id!r} for group {group['id']!r}")
        price += option["priceDelta"]
        summary.append({"groupId": group["id"], "optionId": option["id"], "optionLabel": option["label"]})

    return {"product": product, "unit_price": price, "selection_summary": summary}
