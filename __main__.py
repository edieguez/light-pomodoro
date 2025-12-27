#! /usr/bin/env python3

"""Main entry point for the Pomodoro application."""

import os

from pomodoro.pomodoro import Pomodoro
import util.config


if __name__ == "__main__":
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config/pomodoro.yaml")

    config = util.config.Config(CONFIG_FILE_PATH)
    smart_bulb = config.get_smart_bulb()
    desktop_notifier = config.get_desktop_notifier()
    pomodoro_conf = config.get_pomodoro(config.args.pomodoro)

    pomodoro = Pomodoro(smart_bulb, desktop_notifier, pomodoro_conf)
    pomodoro.start()
