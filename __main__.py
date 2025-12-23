#! /usr/bin/env python3

"""Main entry point for the Pomodoro application."""

import os

from pomodoro.pomodoro import Pomodoro
import util.config


if __name__ == "__main__":
    args = util.config.parse_args()

    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config/pomodoro.json")

    smart_bulb_conf, pomodoro_conf = util.config.read_config(args.bulb, CONFIG_FILE_PATH)
    pomodoro = Pomodoro(smart_bulb_conf, pomodoro_conf)
    pomodoro.start()
