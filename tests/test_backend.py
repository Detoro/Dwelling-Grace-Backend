import json
import pytest

from app import create_app
from app.data import catalog_pricing, designer_pricing
from app.orders import get_order_by_session_id, init_db, save_order, subscribe_newsletter
from app.routes.checkout import _price_line, CheckoutError


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "DATABASE_URL": "sqlite:///:memory:",
        "STRIPE_SECRET_KEY": "sk_test_mock_dummy_key",
        "STRIPE_WEBHOOK_SECRET": "whsec_mock_dummy_key",
        "FRONTEND_URL": "http://localhost:5173",
    }
    app = create_app(test_config=test_config)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# --- 1. Health & Core Endpoints ---

def test_health_check(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_404_handler(client):
    res = client.get("/api/nonexistent-route")
    assert res.status_code == 404
    data = res.get_json()
    assert "error" in data


# --- 2. Products Catalog API ---

def test_get_all_products(client):
    res = client.get("/api/products")
    assert res.status_code == 200
    products = res.get_json()
    assert isinstance(products, list)
    assert len(products) >= 5
    assert any(p["slug"] == "hearth-pillow" for p in products)


def test_filter_products_by_category(client):
    res = client.get("/api/products?category=pillow")
    assert res.status_code == 200
    products = res.get_json()
    assert all(p["category"] == "pillow" for p in products)


def test_filter_products_by_featured(client):
    res = client.get("/api/products?featured=true")
    assert res.status_code == 200
    products = res.get_json()
    assert all(p.get("featured") is True for p in products)


def test_get_product_by_slug(client):
    res = client.get("/api/products/hearth-pillow")
    assert res.status_code == 200
    data = res.get_json()
    assert data["slug"] == "hearth-pillow"
    assert data["name"] == "Hearth Pillow"


def test_get_product_by_invalid_slug(client):
    res = client.get("/api/products/unknown-product-slug")
    assert res.status_code == 404


# --- 3. 3D Designer Pricing & Options ---

def test_designer_pillow_base_pricing():
    config = {
        "fabricId": "linen-oat",
        "sizeId": "18x18",
        "pipingId": "piping-none",
        "closureId": "closure-hidden-zip",
    }
    price = designer_pricing.compute_pillow_price(config)
    assert price == 1899


def test_designer_pillow_midnight_velvet_and_large_size():
    config = {
        "fabricId": "velvet-navy",
        "sizeId": "24x24",
        "pipingId": "piping-contrast",
        "closureId": "closure-button",
    }
    price = designer_pricing.compute_pillow_price(config)
    assert price == 1899 + 2200 + 1100 + 1400 + 1100


def test_designer_pillow_floral_jacquard():
    config = {
        "fabricId": "floral-jacquard",
        "sizeId": "20x20",
        "pipingId": "piping-self",
        "closureId": "closure-envelope",
    }
    price = designer_pricing.compute_pillow_price(config)
    assert price == 1899 + 4800 + 600 + 900


def test_designer_pillow_monogram_textures():
    base_config = {
        "fabricId": "linen-clay",
        "sizeId": "18x18",
        "pipingId": "piping-none",
        "closureId": "closure-hidden-zip",
        "monogram": "ABC",
    }

    # Satin texture (+1400)
    config_satin = {**base_config, "monogramTexture": "satin"}
    assert designer_pricing.compute_pillow_price(config_satin) == 1899 + 1400

    # Silk texture (+1800)
    config_silk = {**base_config, "monogramTexture": "silk"}
    assert designer_pricing.compute_pillow_price(config_silk) == 1899 + 1800

    # Metallic texture (+2200)
    config_metallic = {**base_config, "monogramTexture": "metallic"}
    assert designer_pricing.compute_pillow_price(config_metallic) == 1899 + 2200


def test_designer_pillow_without_tassel_does_not_crash():
    config = {
        "fabricId": "velvet-wine",
        "sizeId": "18x18",
        "pipingId": "piping-none",
        "closureId": "closure-hidden-zip",
    }
    price = designer_pricing.compute_pillow_price(config)
    assert price == 1899 + 2200

    summary = designer_pricing.pillow_selection_summary(config)
    assert len(summary) == 4
    assert any(s["groupId"] == "fabric" and s["optionId"] == "velvet-wine" for s in summary)


def test_designer_case_pricing():
    config = {
        "fabricId": "silk-gold",
        "sizeId": "king",
        "closureId": "closure-envelope",
    }
    price = designer_pricing.compute_case_price(config)
    assert price == 5800 + 4800 + 800

    summary = designer_pricing.case_selection_summary(config)
    assert len(summary) == 3


def test_designer_invalid_option():
    with pytest.raises(designer_pricing.InvalidOptionError):
        designer_pricing.compute_pillow_price({
            "fabricId": "invalid-fabric",
            "sizeId": "18x18",
            "pipingId": "piping-none",
            "closureId": "closure-hidden-zip",
        })


# --- 4. Catalog Pricing ---

def test_catalog_pricing_valid():
    priced = catalog_pricing.price_catalog_line(
        "prod-pillow-hearth",
        {"fabric": "linen-clay", "size": "20x20"},
    )
    assert priced["product"]["slug"] == "hearth-pillow"
    assert priced["unit_price"] == 9800 + 800


def test_catalog_pricing_missing_required():
    with pytest.raises(catalog_pricing.InvalidLineError, match="Missing required selection"):
        catalog_pricing.price_catalog_line(
            "prod-pillow-hearth",
            {"fabric": "linen-clay"},
        )


def test_catalog_pricing_invalid_option():
    with pytest.raises(catalog_pricing.InvalidLineError, match="Unknown option"):
        catalog_pricing.price_catalog_line(
            "prod-pillow-hearth",
            {"fabric": "invalid-option", "size": "18x18"},
        )


# --- 5. Checkout Line Pricing & Validation ---

def test_price_line_custom_pillow_frontend_payload():
    raw_line = {
        "productId": "custom-pillow",
        "quantity": 2,
        "designerConfig": {
            "fabricId": "velvet-navy",
            "sizeId": "24x24",
            "pipingId": "piping-contrast",
            "closureId": "closure-button",
            "monogram": "TD",
            "monogramFont": "serif",
            "monogramTexture": "metallic",
        },
    }
    line = _price_line(raw_line)
    assert line["quantity"] == 2
    assert "Custom Pillow (monogram: TD)" in line["name"]
    expected_unit = 1899 + 2200 + 1100 + 1400 + 1100 + 2200
    assert line["unit_price"] == expected_unit


def test_price_line_invalid_quantity():
    with pytest.raises(CheckoutError, match="Invalid quantity"):
        _price_line({"productId": "custom-pillow", "quantity": 0})

    with pytest.raises(CheckoutError, match="Invalid quantity"):
        _price_line({"productId": "custom-pillow", "quantity": 25})


def test_create_session_empty_bag(client):
    res = client.post("/api/checkout/session", json={"lines": []})
    assert res.status_code == 400
    assert res.get_json()["error"] == "Your bag is empty."


# --- 6. Database Operations (Orders & Newsletter) ---

def test_orders_db_operations():
    db_uri = "sqlite:///:memory:"
    init_db(db_uri)

    session_id = "cs_test_12345"
    order_id = "TD-TEST01"
    email = "test@example.com"
    total = 5400
    lines = [{"name": "Custom Pillow", "quantity": 1, "unitPrice": 5400}]

    save_order(db_uri, session_id, order_id, email, total, lines)

    retrieved = get_order_by_session_id(db_uri, session_id)
    assert retrieved is not None
    assert retrieved["orderId"] == order_id
    assert retrieved["email"] == email
    assert retrieved["total"] == total
    assert retrieved["lines"] == lines


def test_newsletter_db_subscription():
    db_uri = "sqlite:///:memory:"
    init_db(db_uri)

    assert subscribe_newsletter(db_uri, "subscriber@example.com") is True
    assert subscribe_newsletter(db_uri, "subscriber@example.com") is True

    with pytest.raises(ValueError):
        subscribe_newsletter(db_uri, "not-an-email")


# --- 7. Newsletter API Endpoint ---

def test_newsletter_endpoint_success(client):
    res = client.post("/api/newsletter", json={"email": "reader@thistleanddown.com"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "subscribed"
    assert data["email"] == "reader@thistleanddown.com"


def test_newsletter_endpoint_invalid_email(client):
    res = client.post("/api/newsletter", json={"email": "invalid"})
    assert res.status_code == 400
    assert "error" in res.get_json()

    res2 = client.post("/api/newsletter", json={})
    assert res2.status_code == 400


# --- 8. Designer Options Dynamic Endpoint ---

def test_get_designer_options_endpoint(client):
    res = client.get("/api/products/designer-options")
    assert res.status_code == 200
    data = res.get_json()
    assert "fabrics" in data
    assert "sizes" in data
    assert "piping" in data
    assert "closures" in data
    assert "monogramTextures" in data
    assert len(data["fabrics"]) >= 5
    assert any(f["id"] == "velvet-navy" for f in data["fabrics"])
    assert any(s["id"] == "24x24" for s in data["sizes"])
