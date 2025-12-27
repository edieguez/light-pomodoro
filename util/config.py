"""Pomodoro utility functions"""

import yaml
from argparse import ArgumentParser, Namespace

from pomodoro.models import SmartBulbConfig, PomodoroConfig, ThemeConfig
from notification.notification import NoOpBulbNotifier, SmartBulbNotifier, DesktopNotifier, NoOpDesktopNotifier


def parse_args() -> Namespace:
    """Parse command line arguments."""
    parser = ArgumentParser(description="Pomodoro Timer with Smart Bulb Integration")

    bulb_group = parser.add_mutually_exclusive_group()
    bulb_group.add_argument(
        "-b",
        "--bulb",
        type=str,
        default=None,
        help=(
            "Name of the smart bulb to use. "
            "Defaults to the first smart bulb found in the configuration file."
        ),
    )
    bulb_group.add_argument(
        "-B",
        "--no-bulb",
        action="store_true",
        help="Do not use a smart bulb for Pomodoro notifications.",
    )

    parser.add_argument(
        "-p",
        "--pomodoro",
        type=str,
        default=None,
        help=(
            "Pomodoro configuration to use. "
            "This affects work duration, break duration and cycle count. "
            "Defaults to the first Pomodoro found in the configuration file."
        ),
    )
    parser.add_argument(
        "-t",
        "--theme",
        type=str,
        default=None,
        help=(
            "Theme to use for the smart bulb colors. "
            "Defaults to the first theme found in the configuration file."
        ),
    )
    parser.add_argument(
        "-N",
        "--no-desktop-notification",
        action="store_true",
        help="Do not use desktop notifications for Pomodoro events.",
    )

    return parser.parse_args()

class Config:
    """Read and parse Pomodoro configuration from a JSON file"""

    def __init__(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as file:
            self.raw_config = yaml.safe_load(file)

        self.args = parse_args()

    def get_smart_bulb(self) -> SmartBulbNotifier | NoOpBulbNotifier:
        """Retrieve the SmartBulbNotifier based on command line arguments."""
        if self.args.no_bulb:
            return NoOpBulbNotifier()

        available_bulbs = self.raw_config.get("smart_bulbs", [])

        if not available_bulbs:
            raise ValueError("No smart bulbs found in configuration file.")

        theme: ThemeConfig = self.get_theme(self.args.theme)

        if self.args.bulb is None:
            return SmartBulbNotifier(SmartBulbConfig(**available_bulbs[0]), theme)

        for smart_bulb in available_bulbs:
            if smart_bulb.get("name").lower() == self.args.bulb.lower():
                return SmartBulbNotifier(SmartBulbConfig(**smart_bulb), theme)

        raise ValueError(f"Smart bulb with name '{self.args.bulb}' not found.")

    def get_desktop_notifier(self) -> DesktopNotifier | NoOpDesktopNotifier:
        """Retrieve the desktop notifier based on command line arguments."""
        if self.args.no_desktop_notification:
            return NoOpDesktopNotifier()

        return DesktopNotifier()

    def get_pomodoro(self, pomodoro_name: str | None) -> PomodoroConfig:
        """Retrieve the PomodoroConfig from the configuration file."""
        available_pomodoros = self.raw_config.get("pomodoros", [])

        if not available_pomodoros:
            raise ValueError("No pomodoro configurations found in configuration file.")

        if pomodoro_name is None:
            return PomodoroConfig(**available_pomodoros[0])

        for pomodoro in available_pomodoros:
            if pomodoro.get("name").lower() == pomodoro_name.lower():
                return PomodoroConfig(**pomodoro)

        raise ValueError(f"Pomodoro configuration with name '{pomodoro_name}' not found.")

    def get_theme(self, theme_name: str | None) -> ThemeConfig:
        """Retrieve a theme configuration by name from the configuration file."""
        available_themes = self.raw_config.get("themes", [])

        if not available_themes:
            raise ValueError("No themes found in configuration file.")

        if theme_name is None:
            return ThemeConfig(**available_themes[0])

        for theme in available_themes:
            if theme.get("name").lower() == theme_name.lower():
                return ThemeConfig(**theme)

        raise ValueError(f"Theme with name '{theme_name}' not found.")
