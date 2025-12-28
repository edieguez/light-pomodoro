"""Main Pomodoro application logic"""

import time

from notification.notification import (NoOpBulbNotifier, SmartBulbNotifier,
                                       DesktopNotifier, NoOpDesktopNotifier)
from pomodoro.models import PomodoroConfig


class Pomodoro:
    """Pomodoro application class"""

    def __init__(self, smart_bulb_notifier: SmartBulbNotifier | NoOpBulbNotifier,
                 desktop_notifier: DesktopNotifier | NoOpDesktopNotifier,
                 pomodoro_config: PomodoroConfig):
        self.smart_bulb_notifier = smart_bulb_notifier
        self.desktop_notifier = desktop_notifier
        self.config: PomodoroConfig = pomodoro_config

    def start(self):
        """Starts the Pomodoro timer."""
        print("🍅 Pomodoro timer started")
        print(
            f"🍅 {self.config.name.title()} | ⏰ {self.config.duration} min | "
            f"☕️ {self.config.short_break} min | 🌴 {self.config.long_break} min | "
            f"🔄 {self.config.cycles_before_long_break}"
        )

        cycle_count = 0
        pomodoro_count = 0

        try:
            while True:
                cycle_count += 1

                self.work_session(cycle_count, pomodoro_count)

                if cycle_count % self.config.cycles_before_long_break == 0:
                    self.long_break(cycle_count, pomodoro_count)
                    pomodoro_count += 1
                    cycle_count = 0
                else:
                    self.short_break(cycle_count, pomodoro_count)
        except KeyboardInterrupt:
            print("\n🛑 Pomodoro timer stopped by user")
            self.smart_bulb_notifier.turn_off()

    def work_session(self, cycle: int, pomodoro_count: int):
        """Execute a work session with the configured duration and color."""
        self.desktop_notifier.work_notification()
        self.smart_bulb_notifier.work_notification()

        self._countdown(
            self.config.duration,
            f"⏰ Work session | 🍅 {pomodoro_count:02d} - "
            f"🔄 {cycle:02d}/{self.config.cycles_before_long_break:02d}",
            "✅ Work session completed!"
        )

    def short_break(self, cycle: int, pomodoro_count: int):
        """Execute a short break with the configured duration and color."""
        self.desktop_notifier.short_break_notification()
        self.smart_bulb_notifier.short_break_notification()

        self._countdown(
            self.config.short_break,
            f"☕️ Short break | 🍅 {pomodoro_count:02d} - "
            f"🔄 {cycle:02d}/{self.config.cycles_before_long_break:02d}",
            "✅ Short break completed!"
        )

    def long_break(self, cycle: int, pomodoro_count: int):
        """Execute a long break with the configured duration and color."""
        self.desktop_notifier.long_break_notification()
        self.smart_bulb_notifier.long_break_notification()

        self._countdown(
            self.config.long_break,
            f"🌴 Long break | 🍅 {pomodoro_count:02d} - "
            f"🔄 {cycle:02d}/{self.config.cycles_before_long_break:02d}",
            "✅ Long break completed!"
        )

    def _countdown(self, duration_minutes: int, phase_label: str, completion_msg: str):
        """Countdown timer that displays remaining time in place."""
        total_seconds = duration_minutes * 60

        for remaining in range(total_seconds, 0, -1):
            minutes, seconds = divmod(remaining, 60)
            time_str = f"{minutes:02d}:{seconds:02d}"

            # Clear and update display (single line)
            print(f"\033[K{phase_label} | ⏱️ {time_str}", end="", flush=True)
            print("\r", end="")  # Return to start of line

            time.sleep(1)

        # Display completion message
        print(f"\033[K{completion_msg}\r", flush=True, end="")

        time.sleep(1.5)  # Show completion message briefly
