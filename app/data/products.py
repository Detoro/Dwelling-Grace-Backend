PRODUCTS = [
    {
        "id": "prod-pillow-hearth",
        "slug": "hearth-pillow",
        "name": "Hearth Pillow",
        "category": "pillow",
        "basePrice": 9800,
        "images": [
            "/images/hearth-pillow-1.jpg",
            "/images/hearth-pillow-2.jpg",
        ],
        "shortDescription": "Our best-selling square pillow, in your choice of fabric and size.",
        "description": (
            "A simple, well-proportioned square pillow built the same way we build every "
            "piece — cut and stitched to order, in small batches, from fabric we keep on "
            "hand in the workroom."
        ),
        "variantGroups": [
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
                    {"id": "14x14", "label": '14" × 14"', "priceDelta": -600},
                    {"id": "18x18", "label": '18" × 18"', "priceDelta": 0},
                    {"id": "20x20", "label": '20" × 20"', "priceDelta": 800},
                    {"id": "12x20-lumbar", "label": '12" × 20" Lumbar', "priceDelta": 600},
                ],
            },
        ],
        "careNotes": "Spot clean with a damp cloth. Dry clean only for velvet and silk covers.",
        "shippingNotes": "Made to order — ships in 2–3 weeks. Free shipping over $150.",
        "featured": True,
    },
    {
        "id": "prod-pillow-orchard",
        "slug": "orchard-lumbar-pillow",
        "name": "Orchard Lumbar Pillow",
        "category": "pillow",
        "basePrice": 10400,
        "images": ["/images/orchard-lumbar-1.jpg"],
        "shortDescription": "A long lumbar shape for a reading chair or a window seat.",
        "description": (
            "Built on the same frame as the Hearth Pillow but cut long and narrow — made "
            "for the small of your back on a deep chair, or laid flat along a windowsill."
        ),
        "variantGroups": [
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
        ],
        "careNotes": "Spot clean with a damp cloth. Dry clean only for velvet covers.",
        "shippingNotes": "Made to order — ships in 2–3 weeks. Free shipping over $150.",
        "featured": True,
    },
    {
        "id": "prod-case-standard",
        "slug": "everyday-pillowcase-set",
        "name": "Everyday Pillowcase Set",
        "category": "pillowcase",
        "basePrice": 5800,
        "images": ["/images/pillowcase-set-1.jpg"],
        "shortDescription": "A set of two cases, in the same fabrics as the pillows.",
        "description": (
            "The same linen and velvet as the rest of the collection, cut into a simple "
            "envelope-back case. Sold as a set of two."
        ),
        "variantGroups": [
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
        "careNotes": "Machine wash cold, tumble dry low.",
        "shippingNotes": "Made to order — ships in 2–3 weeks. Free shipping over $150.",
        "featured": False,
    },
    {
        "id": "prod-accessory-insert",
        "slug": "feather-down-insert",
        "name": "Feather-Down Insert",
        "category": "accessory",
        "basePrice": 2600,
        "images": ["/images/insert-1.jpg"],
        "shortDescription": "A 95/5 feather-down insert, sized to fit any of our covers.",
        "description": "A generously filled 95% feather, 5% down insert so your cover keeps its shape.",
        "variantGroups": [
            {
                "id": "size",
                "label": "Size",
                "required": True,
                "options": [
                    {"id": "14x14", "label": '14" × 14"', "priceDelta": 0},
                    {"id": "18x18", "label": '18" × 18"', "priceDelta": 400},
                    {"id": "20x20", "label": '20" × 20"', "priceDelta": 700},
                    {"id": "12x20-lumbar", "label": '12" × 20" Lumbar', "priceDelta": 500},
                ],
            },
        ],
        "careNotes": "Spot clean only. Air out in sun periodically to keep it lofted.",
        "shippingNotes": "Ships within 3–5 business days — not made to order.",
        "featured": True,
    },
    {
        "id": "prod-accessory-monogram",
        "slug": "monogram-add-on",
        "name": "Monogram Add-On",
        "category": "accessory",
        "basePrice": 1200,
        "images": ["/images/monogram-1.jpg"],
        "shortDescription": "Hand-embroidered initials for any pillow or case, up to three letters.",
        "description": "Add up to three hand-embroidered initials to any pillow or case in your order.",
        "variantGroups": [],
        "careNotes": "Spot clean around embroidery; avoid direct ironing over stitching.",
        "shippingNotes": "Adds no extra time — bundled with the item it's attached to.",
        "featured": False,
    },
]


def all_products():
    return PRODUCTS


def find_by_slug(slug: str):
    return next((p for p in PRODUCTS if p["slug"] == slug), None)


def find_by_id(product_id: str):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def filter_products(category: str | None = None, featured: bool | None = None):
    products = PRODUCTS
    if category:
        products = [p for p in products if p["category"] == category]
    if featured is not None:
        products = [p for p in products if p.get("featured", False) == featured]
    return products
