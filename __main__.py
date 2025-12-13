#! /usr/bin/env python3

"""Main entry point for the Pomodoro application."""

from pomodoro.pomodoro import Pomodoro
import util.config


if __name__ == "__main__":
    CONFIG_FILE_PATH = "config/pomodoro.json"

    smart_bulb_conf, pomodoro_conf = util.config.read_config(CONFIG_FILE_PATH)
    pomodoro = Pomodoro(smart_bulb_conf, pomodoro_conf)
    pomodoro.start()
