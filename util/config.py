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

class Config:
    """Read and parse Pomodoro configuration from a JSON file"""

    def __init__(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as file:
            self.raw_config = json.load(file)

    def get_smart_bulb(self, bulb_name: str | None) -> SmartBulbConfig:
        """Retrieve a SmartBulbConfig by name from the configuration file."""
        available_bulbs = self.raw_config.get("smart_bulbs", [])

        if not available_bulbs:
            raise ValueError("No smart bulbs found in configuration file.")

        if bulb_name is None:
            return SmartBulbConfig(**available_bulbs[0])

        for smart_bulb in available_bulbs:
            if smart_bulb.get("name").lower() == bulb_name.lower():
                return SmartBulbConfig(**smart_bulb)

        raise ValueError(f"Smart bulb with name '{bulb_name}' not found.")

    def get_pomodoro(self) -> PomodoroConfig:
        """Retrieve the PomodoroConfig from the configuration file."""
        return PomodoroConfig(**self.raw_config.get("pomodoro"))
