"""Functions to generate DPS raw payloads"""
import json

from pomodoro.models import PhaseColor


def generate_payload(phase_color: PhaseColor) -> dict[str, object]:
    """Generate payload for setting smart bulb color based on RGB values."""
    r, g, b = phase_color.color
    saturation = phase_color.saturation
    brightness = phase_color.brightness
    temperature = phase_color.temperature
    dps = phase_color.dps

    if dps:
        return json.loads(dps)

    if r == g == b == 255:
        # White mode
        return {
            "20": True,
            "21": "white",
            "22": brightness,
            "23": temperature,
        }

    if r == g == b == 0:
        # There is not a pure black mode, so we turn off the bulb
        return {
            "20": False
        }

    return {
        "20": True,
        "21": "colour",
        "24": encode_colour(
            rgb_to_hue(r, g, b),
            saturation,
            brightness
        )
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
