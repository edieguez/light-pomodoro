"""Main Pomodoro application logic"""

import json
from tinytuya import BulbDevice

from pomodoro.models import PomodoroConfig, SmartBulbConfig


class Pomodoro:
    """Pomodoro application class"""

    def __init__(self, smart_bulb_config: SmartBulbConfig, pomodoro_config: PomodoroConfig):
        self.smart_bulb = BulbDevice(
            dev_id=smart_bulb_config.device_id,
            address=smart_bulb_config.address,
            local_key=smart_bulb_config.local_key,
            version=smart_bulb_config.version,
        )
        self.pomodoro = pomodoro_config

    def start(self):
        """Starts the Pomodoro timer."""
        print("Pomodoro started!")
        print(json.dumps(self.smart_bulb.status(), indent=4))
        self.smart_bulb.set_colour(128, 1, 128)
