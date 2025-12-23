"""Pomodoro utility functions"""

import json
from argparse import ArgumentParser, Namespace

from pomodoro.models import SmartBulbConfig, PomodoroConfig


def parse_args() -> Namespace:
    """Parse command line arguments."""
    parser = ArgumentParser(description="Pomodoro Timer with Smart Bulb Integration")

    parser.add_argument(
        "-b",
        "--bulb",
        type=str,
        default=None,
        help=(
            "Name of the smart bulb to use. "
            "If not provided, the first bulb in the configuration file will be used."
        ),
    )

    return parser.parse_args()

def read_config(bulb_name: str, file_path: str) -> tuple[SmartBulbConfig, PomodoroConfig]:
    """Reads a JSON configuration file and returns its contents as a tuple of
    SmartBulbConfig and PomodoroConfig instances."""

    with open(file_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    available_bulbs = config.get("smart_bulbs", [])

    if not available_bulbs:
        raise ValueError("No smart bulbs found in configuration file.")

    smart_bulb = _get_smart_bulb(bulb_name, available_bulbs)
    pomodoro = PomodoroConfig(**config.get("pomodoro"))

    return smart_bulb, pomodoro

def _get_smart_bulb(bulb_name: str | None, smart_bulbs: list[dict[str, object]]) -> SmartBulbConfig:
    """Retrieve a SmartBulbConfig by name from the configuration file."""
    if bulb_name is None:
        return SmartBulbConfig(**smart_bulbs[0])

    for smart_bulb in smart_bulbs:
        if smart_bulb.get("name").lower() == bulb_name.lower():
            return SmartBulbConfig(**smart_bulb)

    raise ValueError(f"Smart bulb with name '{bulb_name}' not found.")