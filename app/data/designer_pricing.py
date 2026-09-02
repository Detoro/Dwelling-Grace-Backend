"""
Pricing for the Pillow / Pillowcase Designer.

Mirrors src/data/designerOptions.ts on the frontend. That copy exists so
the UI can show a live price as someone picks options; this copy is what
actually gets charged.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class Option:
    id: str
    label: str
    price_delta: int


FABRICS = [
    Option("linen-oat", "Oat Linen", 0),
    Option("linen-clay", "Clay Linen", 0),
    Option("velvet-navy", "Midnight Velvet", 2200),
    Option("velvet-wine", "Wine Velvet", 2200),
    Option("velvet-moss", "Moss Velvet", 2200),
    Option("silk-gold", "Gold Silk", 4800),
    Option("floral-jacquard", "Floral Jacquard", 4800),
]

SIZES = [
    Option("18x18", '18" × 18"', 0),
    Option("20x20", '20" × 20"', 600),
    Option("24x24", '24" × 24"', 1100),
    Option("14x14", '14" × 14"', -600),
    Option("12x20-lumbar", '12" × 20" Lumbar', 600),
]

PIPING = [
    Option("piping-none", "No piping", 0),
    Option("piping-self", "Self-fabric piping", 900),
    Option("piping-contrast", "Contrast piping", 1400),
]

TASSELS = [
    Option("tassel-none", "No tassels", 0),
    Option("tassel-corner", "Corner tassels", 1800),
    Option("tassel-fringe", "Full fringe trim", 3200),
]

CLOSURES = [
    Option("closure-hidden-zip", "Hidden zip", 0),
    Option("closure-button", "Horn buttons", 1100),
    Option("closure-envelope", "Envelope back", 0),
]

MONOGRAM_FONTS = [
    Option("serif", "Classic Serif", 0),
    Option("script", "Artisanal Script", 0),
    Option("sans", "Modern Sans", 0),
    Option("mono", "Architectural Mono", 0),
]

MONOGRAM_TEXTURES = [
    Option("satin", "Satin Stitch", 1400),
    Option("silk", "Silk Floss", 1800),
    Option("cotton", "Matte Cotton", 1400),
    Option("metallic", "Metallic Gilt", 2200),
]

CASE_SIZES = [
    Option("standard", 'Standard (20" × 26")', 0),
    Option("queen", 'Queen (20" × 30")', 400),
    Option("king", 'King (20" × 36")', 800),
]

PILLOW_BASE_PRICE = 1899
CASE_BASE_PRICE = 5800


class InvalidOptionError(ValueError):
    pass


def find_option(options: List[Option], option_id: str) -> Option:
    for option in options:
        if option.id == option_id:
            return option
    raise InvalidOptionError(f"Unknown option id: {option_id!r}")


def compute_pillow_price(config: Dict[str, Any]) -> int:
    """
    config keys: fabricId, sizeId, pipingId, closureId,
    monogram (optional), monogramTexture (optional), tasselId (optional)
    """
    fabric = find_option(FABRICS, config["fabricId"])
    size = find_option(SIZES, config["sizeId"])
    piping = find_option(PIPING, config["pipingId"])
    closure = find_option(CLOSURES, config["closureId"])

    price = PILLOW_BASE_PRICE + fabric.price_delta + size.price_delta + piping.price_delta + closure.price_delta

    tassel_id = config.get("tasselId")
    if tassel_id and tassel_id != "tassel-none":
        tassel = find_option(TASSELS, tassel_id)
        price += tassel.price_delta

    monogram_text = str(config.get("monogram", "") or "").strip()
    if monogram_text:
        tex_id = config.get("monogramTexture", "satin")
        texture = next((t for t in MONOGRAM_TEXTURES if t.id == tex_id), None)
        monogram_price = texture.price_delta if texture is not None else 1400
        price += monogram_price

    return price


def compute_case_price(config: Dict[str, Any]) -> int:
    """config keys: fabricId, sizeId, closureId, monogram (optional)"""
    fabric = find_option(FABRICS, config["fabricId"])
    size = find_option(CASE_SIZES, config["sizeId"])
    closure = find_option(CLOSURES, config["closureId"])

    price = CASE_BASE_PRICE + fabric.price_delta + size.price_delta + closure.price_delta
    return price


def pillow_selection_summary(config: Dict[str, Any]) -> List[Dict[str, str]]:
    fabric = find_option(FABRICS, config["fabricId"])
    size = find_option(SIZES, config["sizeId"])
    piping = find_option(PIPING, config["pipingId"])
    closure = find_option(CLOSURES, config["closureId"])

    summary = [
        {"groupId": "fabric", "optionId": fabric.id, "optionLabel": fabric.label},
        {"groupId": "size", "optionId": size.id, "optionLabel": size.label},
        {"groupId": "piping", "optionId": piping.id, "optionLabel": piping.label},
        {"groupId": "closure", "optionId": closure.id, "optionLabel": closure.label},
    ]

    tassel_id = config.get("tasselId")
    if tassel_id and tassel_id != "tassel-none":
        tassel = find_option(TASSELS, tassel_id)
        summary.append({"groupId": "tassel", "optionId": tassel.id, "optionLabel": tassel.label})

    monogram_text = str(config.get("monogram", "") or "").strip()
    if monogram_text:
        font_id = config.get("monogramFont", "serif")
        font_opt = next((f for f in MONOGRAM_FONTS if f.id == font_id), MONOGRAM_FONTS[0])
        tex_id = config.get("monogramTexture", "satin")
        tex_opt = next((t for t in MONOGRAM_TEXTURES if t.id == tex_id), MONOGRAM_TEXTURES[0])
        summary.append({
            "groupId": "monogram",
            "optionId": "custom",
            "optionLabel": f'Monogram "{monogram_text.upper()}" ({font_opt.label}, {tex_opt.label})',
        })

    return summary


def case_selection_summary(config: Dict[str, Any]) -> List[Dict[str, str]]:
    fabric = find_option(FABRICS, config["fabricId"])
    size = find_option(CASE_SIZES, config["sizeId"])
    closure = find_option(CLOSURES, config["closureId"])
    return [
        {"groupId": "fabric", "optionId": fabric.id, "optionLabel": fabric.label},
        {"groupId": "size", "optionId": size.id, "optionLabel": size.label},
        {"groupId": "closure", "optionId": closure.id, "optionLabel": closure.label},
    ]
