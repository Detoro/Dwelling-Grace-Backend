from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class Option:
    id: str
    label: str
    price_delta: int


FABRICS = [
    Option("linen-oat", "Oat Linen", 0),
    Option("velvet-navy", "Midnight Velvet", 2200),
    Option("velvet-wine", "Wine Velvet", 2200),
    Option("silk-gold", "Gold Silk", 4800),
    Option("floral-jacquard", "Floral Jacquard", 4800),
]

SIZES = [
    Option("18x18", '18" × 18"', 0),
    Option("20x20", '20" × 20"', 600),
    Option("24x24", '24" × 24"', 1100),
]

MONOGRAM_FONTS = [
    Option("serif", "Classic Serif", 0),
    Option("script", "Artisanal Script", 0),
    Option("sans", "Modern Sans", 0),
    Option("mono", "Architectural Mono", 0),
    Option("futura", "Futura Geometric", 0),
]

MONOGRAM_TEXTURES = [
    Option("satin", "Satin Stitch", 1400),
    Option("silk", "Silk Floss", 1800),
    Option("cotton", "Matte Cotton", 1400),
    Option("metallic", "Metallic Gilt", 2200)
]

CASE_SIZES = [
    Option("standard", 'Standard (20" × 26")', 0),
    Option("queen", 'Queen (20" × 30")', 400),
    Option("king", 'King (20" × 36")', 800)
]

CASE_BASE_PRICE = 1499


class InvalidOptionError(ValueError):
    pass


def find_option(options: List[Option], option_id: str) -> Option:
    for option in options:
        if option.id == option_id:
            return option
    raise InvalidOptionError(f"Unknown option id: {option_id!r}")


def compute_case_price(config: Dict[str, Any]) -> int:
    fabric = find_option(FABRICS, config["fabricId"])
    size = find_option(CASE_SIZES, config["sizeId"])

    price = CASE_BASE_PRICE + fabric.price_delta + size.price_delta
    return price


def pillow_selection_summary(config: Dict[str, Any]) -> List[Dict[str, str]]:
    fabric = find_option(FABRICS, config["fabricId"])
    size = find_option(SIZES, config["sizeId"])

    summary = [
        {"groupId": "fabric", "optionId": fabric.id, "optionLabel": fabric.label},
        {"groupId": "size", "optionId": size.id, "optionLabel": size.label},
    ]

    monogram_text = str(config.get("monogram", "") or "").strip()
    if monogram_text:
        font_id = config.get("monogramFont", "serif")
        font_opt = next((f for f in MONOGRAM_FONTS if f.id == font_id), MONOGRAM_FONTS[0])
        tex_id = config.get("monogramTexture", "satin")
        tex_opt = next((t for t in MONOGRAM_TEXTURES if t.id == tex_id), MONOGRAM_TEXTURES[0])
        summary.append({
            "groupId": "monogram",
            "optionId": "custom",
            "optionLabel": f'Monogram "{monogram_text.upper()}" ({font_opt.label}, {tex_opt.label})'
        })

    return summary


def case_selection_summary(config: Dict[str, Any]) -> List[Dict[str, str]]:
    fabric = find_option(FABRICS, config["fabricId"])
    size = find_option(CASE_SIZES, config["sizeId"])
    return [
        {"groupId": "fabric", "optionId": fabric.id, "optionLabel": fabric.label},
        {"groupId": "size", "optionId": size.id, "optionLabel": size.label}
    ]
