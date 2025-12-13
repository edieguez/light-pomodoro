"""Main Pomodoro application logic"""

import json
import time
from tinytuya import BulbDevice

from pomodoro.models import PomodoroConfig, SmartBulbConfig


class Pomodoro:
    """Pomodoro application class"""

    def __init__(self, smart_bulb_config: SmartBulbConfig, pomodoro_config: PomodoroConfig):
        self.smart_bulb: BulbDevice = BulbDevice(
            dev_id=smart_bulb_config.device_id,
            address=smart_bulb_config.address,
            local_key=smart_bulb_config.local_key,
            version=smart_bulb_config.version,
        )
        self.pomodoro_config: PomodoroConfig = pomodoro_config

    def start(self):
        """Starts the Pomodoro timer."""
        print("🍅 Pomodoro Timer Started!")
        print(f"Smart Bulb Status: {json.dumps(self.smart_bulb.status(), indent=2)}\n")

        cycle_count = 0

        try:
            while True:
                cycle_count += 1
                print(f"\n{'='*50}")
                print(f"Cycle {cycle_count}")
                print(f"{'='*50}")

                # Work session
                self._work_session()

                # Determine break type
                if cycle_count % self.pomodoro_config.cycles_before_long_break == 0:
                    # Long break after completing the configured number of cycles
                    self._long_break()
                else:
                    # Short break
                    self._short_break()

        except KeyboardInterrupt:
            print("\n\n🛑 Pomodoro Timer stopped by user.")
            self.smart_bulb.turn_off()
            print("Smart bulb turned off. Goodbye!")

    def _work_session(self):
        """Execute a work session with the configured duration and color."""
        print(f"\n⏰ Work Session - {self.pomodoro_config.duration} minutes")

        self.smart_bulb.set_colour(*self.pomodoro_config.color)
        self._countdown(self.pomodoro_config.duration)

        print("✅ Work session completed!")

    def _short_break(self):
        """Execute a short break with the configured duration and color."""
        print(f"\n☕ Short Break - {self.pomodoro_config.short_break.duration} minutes")

        self.smart_bulb.set_colour(*self.pomodoro_config.short_break.color)
        self._countdown(self.pomodoro_config.short_break.duration)

        print("✅ Short break completed!")

    def _long_break(self):
        """Execute a long break with the configured duration and color."""
        print(f"\n🌴 Long Break - {self.pomodoro_config.long_break.duration} minutes")

        self.smart_bulb.set_colour(*self.pomodoro_config.long_break.color)
        self._countdown(self.pomodoro_config.long_break.duration)

        print("✅ Long break completed!")

    def _countdown(self, duration_minutes: int):
        """
        Countdown timer that displays remaining time.

        Args:
            duration_minutes: Duration in minutes
        """
        total_seconds = duration_minutes * 60

        for remaining in range(total_seconds, 0, -1):
            minutes, seconds = divmod(remaining, 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
            print(f"\r⏱️  {time_str} remaining", end="", flush=True)
            time.sleep(1)

        print("\r" + " " * 50, end="")  # Clear the line
        print("\r", end="")
