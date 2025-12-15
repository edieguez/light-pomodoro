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
        print(f"Smart Bulb Status: {json.dumps(self.smart_bulb.status(), indent=2)}")
        print("🍅 Pomodoro timer started")
        print("\n")  # Reserve space for display

        cycle_count = 0
        pomodoro_count = 0

        try:
            while True:
                cycle_count += 1

                # Work session
                self._work_session(cycle_count, pomodoro_count)

                # Determine break type
                if cycle_count % self.pomodoro_config.cycles_before_long_break == 0:
                    # Long break after completing the configured number of cycles
                    self._long_break(cycle_count, pomodoro_count)
                    pomodoro_count += 1
                    cycle_count = 0  # Reset cycle count after long break
                else:
                    # Short break
                    self._short_break(cycle_count, pomodoro_count)

        except KeyboardInterrupt:
            # Move cursor to below the display area
            print("\n")
            print("🛑 Pomodoro timer stopped by user")
            self.smart_bulb.turn_off()

    def _work_session(self, cycle: int, pomodoro_count: int):
        """Execute a work session with the configured duration and color."""

        r, g, b = self.pomodoro_config.color

        if r == g == b == 255:
            # White mode
            self.smart_bulb.set_multiple_values({
                "20": True,
                "21": "white",
                "22": self.pomodoro_config.brightness
            })
        elif r == g == b == 0:
            # There is not a pure black mode, so we turn off the bulb
            self.smart_bulb.set_multiple_values({
                "20": False
            })
        else:
            # Colour mode
            hsv = self._encode_colour(
                self._rgb_to_hue(r, g, b),
                self.pomodoro_config.saturation,
                self.pomodoro_config.brightness
            )

            self.smart_bulb.set_multiple_values({
                "20": True,
                "21": "colour",
                "24": hsv
            })

        self._countdown(
            self.pomodoro_config.duration,
            f"⏰ Work session | 🍅 {pomodoro_count:02d} - 🔄 {cycle:02d}/{self.pomodoro_config.cycles_before_long_break:02d}",
            "✅ Work session completed!"
        )

    def _short_break(self, cycle: int, pomodoro_count: int):
        """Execute a short break with the configured duration and color."""

        self.smart_bulb.set_colour(*self.pomodoro_config.short_break.color, True)
        self.smart_bulb.set_brightness(self.pomodoro_config.short_break.brightness)

        self._countdown(
            self.pomodoro_config.short_break.duration,
            f"☕ Short break | 🍅 {pomodoro_count:02d} - 🔄 {cycle:02d}/{self.pomodoro_config.cycles_before_long_break:02d}",
            "✅ Short break completed!"
        )

    def _long_break(self, cycle: int, pomodoro_count: int):
        """Execute a long break with the configured duration and color."""

        self.smart_bulb.set_colour(*self.pomodoro_config.long_break.color, True)
        self.smart_bulb.set_brightness(self.pomodoro_config.long_break.brightness)

        self._countdown(
            self.pomodoro_config.long_break.duration,
            f"🌴 Long break | 🍅 {pomodoro_count:02d} - 🔄 {cycle:02d}/{self.pomodoro_config.cycles_before_long_break:02d}",
            "✅ Long break completed!"
        )

    def _countdown(self, duration_minutes: int, phase_label: str, completion_msg: str):
        """
        Countdown timer that displays remaining time in place.

        Args:
            duration_minutes: Duration in minutes
            phase_label: Label for the current phase
            completion_msg: Message to display when completed
        """
        total_seconds = duration_minutes * 60

        # Move cursor up 1 line to the display area
        print("\033[1A", end="")

        for remaining in range(total_seconds, 0, -1):
            minutes, seconds = divmod(remaining, 60)
            time_str = f"{minutes:02d}:{seconds:02d}"

            # Clear and update display (single line)
            print("\033[K" + f"{phase_label} | ⏱️ {time_str}", end="", flush=True)
            print("\r", end="")  # Return to start of line

            time.sleep(1)

        # Display completion message
        print("\033[K" + completion_msg, flush=True)

        time.sleep(2)  # Show completion message briefly

    def _rgb_to_hue(self, r: int, g: int, b: int) -> int:
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

    def _encode_colour(self, h: int, s: int, v: int) -> str:
        return f"{h:04x}{s:04x}{v:04x}"
