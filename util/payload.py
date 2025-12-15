"""Functions to generate DPS raw payloads"""

def generate_colour_payload(r: int, g: int, b: int, saturation: int,
                             brightness: int) -> dict[str, object]:
    """Generate payload for setting smart bulb color based on RGB values."""

    if r == g == b == 255:
        # White mode
        return {
            "20": True,
            "21": "white",
            "22": brightness
        }
    elif r == g == b == 0:
        # There is not a pure black mode, so we turn off the bulb
        return {
            "20": False
        }
    else:
        # Colour mode
        hsv = encode_colour(
            rgb_to_hue(r, g, b),
            saturation,
            brightness
        )

        return {
            "20": True,
            "21": "colour",
            "24": hsv
        }

def rgb_to_hue(r: int, g: int, b: int) -> int:
    """Convert RGB values to Hue component in HSV color space."""

    r1, g1, b1 = r / 255, g / 255, b / 255
    cmax = max(r1, g1, b1)
    cmin = min(r1, g1, b1)
    delta = cmax - cmin

    if delta == 0:
        return 0

    if cmax == r1:
        h = 60 * (((g1 - b1) / delta) % 6)
    elif cmax == g1:
        h = 60 * (((b1 - r1) / delta) + 2)
    else:
        h = 60 * (((r1 - g1) / delta) + 4)

    return int(round(h))

def encode_colour(h: int, s: int, v: int) -> str:
    """Encode HSV values into a hexadecimal string payload."""
    return f"{h:04x}{s:04x}{v:04x}"
