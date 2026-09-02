"""
Seed data and seeding logic for Thistle & Down.
Populates the database with initial catalog products and 3D designer options.
"""

import json
from typing import Any, Dict, List

SEED_PRODUCTS: List[Dict[str, Any]] = [
    {
        "id": "prod-pillow-hearth",
        "slug": "hearth-pillow",
        "name": "Hearth Pillow",
        "category": "pillow",
        "base_price": 1899,
        "images": [
            "/pillow__black/textures/Material_baseColor.png",
            "/images/hearth-pillow-1.jpg",
            "/images/hearth-pillow-2.jpg",
        ],
        "short_description": "Our best-selling square pillow, in your choice of fabric and size.",
        "description": (
            "A simple, well-proportioned square pillow built the same way we build every "
            "piece — cut and stitched to order, in small batches, from fabric we keep on "
            "hand in the workroom."
        ),
        "variant_groups": [
            {
                "id": "fabric",
                "label": "Fabric",
                "required": True,
                "options": [
                    {"id": "linen-oat", "label": "Oat Linen", "priceDelta": 0, "swatchHex": "#D8CCB4"},
                    {"id": "linen-clay", "label": "Clay Linen", "priceDelta": 0, "swatchHex": "#B97D5D"},
                    {"id": "velvet-wine", "label": "Wine Velvet", "priceDelta": 2200, "swatchHex": "#5C1F2E"},
                    {"id": "velvet-moss", "label": "Moss Velvet", "priceDelta": 2200, "swatchHex": "#3E4A34"},
                    {"id": "silk-gold", "label": "Gold Silk", "priceDelta": 4800, "swatchHex": "#C7A24C"},
                ],
            },
            {
                "id": "size",
                "label": "Size",
                "required": True,
                "options": [
                    {"id": "18x18", "label": '18" × 18"', "priceDelta": 0},
                    {"id": "20x20", "label": '20" × 20"', "priceDelta": 600},
                    {"id": "24x24", "label": '24" × 24"', "priceDelta": 1100},
                    {"id": "14x14", "label": '14" × 14"', "priceDelta": -600},
                ],
            },
        ],
        "care_notes": "Spot clean with a damp cloth. Dry clean only for velvet and silk covers.",
        "shipping_notes": "Made to order — ships in 2–3 weeks. Free shipping over $150.",
        "featured": True,
    },
    {
        "id": "prod-pillow-orchard",
        "slug": "orchard-lumbar-pillow",
        "name": "Orchard Lumbar Pillow",
        "category": "pillow",
        "base_price": 1899,
        "images": ["/assets/hero.png", "/images/orchard-lumbar-1.jpg"],
        "short_description": "A long lumbar shape for a reading chair or a window seat.",
        "description": (
            "Built on the same frame as the Hearth Pillow but cut long and narrow — made "
            "for the small of your back on a deep chair, or laid flat along a windowsill."
        ),
        "variant_groups": [
            {
                "id": "fabric",
                "label": "Fabric",
                "required": True,
                "options": [
                    {"id": "linen-oat", "label": "Oat Linen", "priceDelta": 0, "swatchHex": "#D8CCB4"},
                    {"id": "linen-clay", "label": "Clay Linen", "priceDelta": 0, "swatchHex": "#B97D5D"},
                    {"id": "velvet-wine", "label": "Wine Velvet", "priceDelta": 2200, "swatchHex": "#5C1F2E"},
                ],
            },
            {
                "id": "piping",
                "label": "Piping",
                "required": False,
                "options": [
                    {"id": "piping-none", "label": "No piping", "priceDelta": 0},
                    {"id": "piping-contrast", "label": "Contrast piping", "priceDelta": 1400, "swatchHex": "#C7A24C"},
                ],
            },
        ],
        "care_notes": "Spot clean with a damp cloth. Dry clean only for velvet covers.",
        "shipping_notes": "Made to order — ships in 2–3 weeks. Free shipping over $150.",
        "featured": True,
    },
    {
        "id": "prod-case-standard",
        "slug": "everyday-pillowcase-set",
        "name": "Everyday Pillowcase Set",
        "category": "pillowcase",
        "base_price": 5800,
        "images": ["/assets/hero.png", "/images/pillowcase-set-1.jpg"],
        "short_description": "A set of two cases, in the same fabrics as the pillows.",
        "description": (
            "The same linen and velvet as the rest of the collection, cut into a simple "
            "envelope-back case. Sold as a set of two."
        ),
        "variant_groups": [
            {
                "id": "fabric",
                "label": "Fabric",
                "required": True,
                "options": [
                    {"id": "linen-oat", "label": "Oat Linen", "priceDelta": 0, "swatchHex": "#D8CCB4"},
                    {"id": "linen-clay", "label": "Clay Linen", "priceDelta": 0, "swatchHex": "#B97D5D"},
                ],
            },
            {
                "id": "size",
                "label": "Size",
                "required": True,
                "options": [
                    {"id": "standard", "label": 'Standard (20" × 26")', "priceDelta": 0},
                    {"id": "queen", "label": 'Queen (20" × 30")', "priceDelta": 400},
                    {"id": "king", "label": 'King (20" × 36")', "priceDelta": 800},
                ],
            },
        ],
        "care_notes": "Machine wash cold, tumble dry low.",
        "shipping_notes": "Made to order — ships in 2–3 weeks. Free shipping over $150.",
        "featured": False,
    },
    {
        "id": "prod-accessory-insert",
        "slug": "feather-down-insert",
        "name": "Feather-Down Insert",
        "category": "accessory",
        "base_price": 2600,
        "images": ["/assets/hero.png", "/images/insert-1.jpg"],
        "short_description": "A 95/5 feather-down insert, sized to fit any of our covers.",
        "description": "A generously filled 95% feather, 5% down insert so your cover keeps its shape.",
        "variant_groups": [
            {
                "id": "size",
                "label": "Size",
                "required": True,
                "options": [
                    {"id": "18x18", "label": '18" × 18"', "priceDelta": 400},
                    {"id": "20x20", "label": '20" × 20"', "priceDelta": 700},
                    {"id": "24x24", "label": '24" × 24"', "priceDelta": 1100},
                    {"id": "14x14", "label": '14" × 14"', "priceDelta": 0},
                ],
            },
        ],
        "care_notes": "Spot clean only. Air out in sun periodically to keep it lofted.",
        "shipping_notes": "Ships within 3–5 business days — not made to order.",
        "featured": True,
    },
    {
        "id": "prod-accessory-monogram",
        "slug": "monogram-add-on",
        "name": "Custom Monogramming",
        "category": "accessory",
        "base_price": 1399,
        "images": ["/assets/hero.png", "/images/monogram-1.jpg"],
        "short_description": "Hand-embroidered initials for any pillow or case, up to three letters.",
        "description": "Add up to three hand-embroidered initials to any pillow or case in your order.",
        "variant_groups": [],
        "care_notes": "Spot clean around embroidery; avoid direct ironing over stitching.",
        "shipping_notes": "Adds no extra time — bundled with the item it's attached to.",
        "featured": False,
    },
]

SEED_DESIGNER_OPTIONS: List[Dict[str, Any]] = [
    # Fabrics
    {"id": "linen-oat", "group_type": "fabric", "label": "Oat Linen", "price_delta": 0, "swatch_hex": "#D8CCB4", "weave": "linen", "display_order": 1},
    {"id": "linen-clay", "group_type": "fabric", "label": "Clay Linen", "price_delta": 0, "swatch_hex": "#B97D5D", "weave": "linen", "display_order": 2},
    {"id": "velvet-navy", "group_type": "fabric", "label": "Midnight Velvet", "price_delta": 2200, "swatch_hex": "#182B49", "weave": "velvet", "display_order": 3},
    {"id": "velvet-wine", "group_type": "fabric", "label": "Wine Velvet", "price_delta": 2200, "swatch_hex": "#5C1F2E", "weave": "velvet", "display_order": 4},
    {"id": "velvet-moss", "group_type": "fabric", "label": "Moss Velvet", "price_delta": 2200, "swatch_hex": "#3E4A34", "weave": "velvet", "display_order": 5},
    {"id": "silk-gold", "group_type": "fabric", "label": "Gold Silk", "price_delta": 4800, "swatch_hex": "#C7A24C", "weave": "silk", "display_order": 6},
    {"id": "floral-jacquard", "group_type": "fabric", "label": "Floral Jacquard", "price_delta": 4800, "swatch_hex": "#C7A24C", "weave": "floral", "display_order": 7},

    # Sizes
    {"id": "18x18", "group_type": "size", "label": '18" × 18"', "price_delta": 0, "display_order": 1},
    {"id": "20x20", "group_type": "size", "label": '20" × 20"', "price_delta": 600, "display_order": 2},
    {"id": "24x24", "group_type": "size", "label": '24" × 24"', "price_delta": 1100, "display_order": 3},
    {"id": "14x14", "group_type": "size", "label": '14" × 14"', "price_delta": -600, "display_order": 4},
    {"id": "12x20-lumbar", "group_type": "size", "label": '12" × 20" Lumbar', "price_delta": 600, "display_order": 5},

    # Piping
    {"id": "piping-none", "group_type": "piping", "label": "No piping", "price_delta": 0, "display_order": 1},
    {"id": "piping-self", "group_type": "piping", "label": "Self-fabric piping", "price_delta": 900, "display_order": 2},
    {"id": "piping-contrast", "group_type": "piping", "label": "Contrast piping", "price_delta": 1400, "swatch_hex": "#C7A24C", "display_order": 3},

    # Closures
    {"id": "closure-hidden-zip", "group_type": "closure", "label": "Hidden zip", "price_delta": 0, "display_order": 1},
    {"id": "closure-button", "group_type": "closure", "label": "Horn buttons", "price_delta": 1100, "display_order": 2},
    {"id": "closure-envelope", "group_type": "closure", "label": "Envelope back", "price_delta": 0, "display_order": 3},

    # Monogram Textures
    {"id": "satin", "group_type": "monogram_texture", "label": "Satin Stitch", "price_delta": 1400, "display_order": 1},
    {"id": "silk", "group_type": "monogram_texture", "label": "Silk Floss", "price_delta": 1800, "display_order": 2},
    {"id": "cotton", "group_type": "monogram_texture", "label": "Matte Cotton", "price_delta": 1400, "display_order": 3},
    {"id": "metallic", "group_type": "monogram_texture", "label": "Metallic Gilt", "price_delta": 2200, "display_order": 4},

    # Monogram Fonts
    {"id": "serif", "group_type": "monogram_font", "label": "Classic Serif", "price_delta": 0, "display_order": 1},
    {"id": "script", "group_type": "monogram_font", "label": "Artisanal Script", "price_delta": 0, "display_order": 2},
    {"id": "sans", "group_type": "monogram_font", "label": "Modern Sans", "price_delta": 0, "display_order": 3},
    {"id": "mono", "group_type": "monogram_font", "label": "Architectural Mono", "price_delta": 0, "display_order": 4},

    # Case Sizes
    {"id": "standard", "group_type": "case_size", "label": 'Standard (20" × 26")', "price_delta": 0, "display_order": 1},
    {"id": "queen", "group_type": "case_size", "label": 'Queen (20" × 30")', "price_delta": 400, "display_order": 2},
    {"id": "king", "group_type": "case_size", "label": 'King (20" × 36")', "price_delta": 800, "display_order": 3},
]


def seed_database(db_uri: str, force: bool = False) -> None:
    from app.orders import DesignerOption, Product, get_session

    session = get_session(db_uri)
    try:
        # Seed Products
        existing_products_count = session.query(Product).count()
        if existing_products_count == 0 or force:
            for p_data in SEED_PRODUCTS:
                existing = session.get(Product, p_data["id"])
                if existing is None:
                    product = Product(
                        id=p_data["id"],
                        slug=p_data["slug"],
                        name=p_data["name"],
                        category=p_data["category"],
                        base_price=p_data["base_price"],
                        images_json=json.dumps(p_data["images"]),
                        short_description=p_data["short_description"],
                        description=p_data["description"],
                        care_notes=p_data["care_notes"],
                        shipping_notes=p_data["shipping_notes"],
                        featured=p_data.get("featured", False),
                        variant_groups_json=json.dumps(p_data["variant_groups"]),
                    )
                    session.add(product)

        # Seed Designer Options
        existing_options_count = session.query(DesignerOption).count()
        if existing_options_count == 0 or force:
            for opt_data in SEED_DESIGNER_OPTIONS:
                existing_opt = session.get(DesignerOption, opt_data["id"])
                if existing_opt is None:
                    opt = DesignerOption(
                        id=opt_data["id"],
                        group_type=opt_data["group_type"],
                        label=opt_data["label"],
                        price_delta=opt_data["price_delta"],
                        swatch_hex=opt_data.get("swatch_hex"),
                        weave=opt_data.get("weave"),
                        display_order=opt_data.get("display_order", 0),
                    )
                    session.add(opt)

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    import os
    from app.config import Config
    from app.orders import init_db

    url = Config.DATABASE_URL
    print(f"Connecting to {url}...")
    init_db(url)
    seed_database(url, force=True)
    print("Database successfully seeded with catalog products and designer options!")

