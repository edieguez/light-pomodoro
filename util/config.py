"""Pomodoro utility functions"""

import json

from pomodoro.models import SmartBulbConfig, PomodoroConfig


def read_config(file_path: str) -> tuple[SmartBulbConfig, PomodoroConfig]:
    """Reads a JSON configuration file and returns its contents as a tuple of
    SmartBulbConfig and PomodoroConfig instances."""

    with open(file_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    smart_bulb = SmartBulbConfig(**config.get("smart_bulb"))
    pomodoro = PomodoroConfig(**config.get("pomodoro"))

    return smart_bulb, pomodoro
