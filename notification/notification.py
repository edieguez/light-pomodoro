"""Module for sending notifications for Pomodoro timer events"""

import os

from notifypy import Notify

class DesktopNotifier:
    """Class for sending desktop notifications"""

    def __init__(self) -> None:
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.notification = Notify(
            default_notification_title="Function Message",
            default_application_name="Great Application",
            default_notification_audio=f"{self.base_dir}/sound/new-notification-09-352705.wav"
        )

    def work_notification(self) -> None:
        """Send a notification for the start of a work session"""
        self.notification.title = "Pomodoro Timer"
        self.notification.message = f"🍅 Work session started!"

        self.notification.send()

    def short_break_notification(self) -> None:
        """Send a notification for the start of a short break"""
        self.notification.title = "Pomodoro Timer"
        self.notification.message = f"☕ Short break started!"

        self.notification.send()

    def long_break_notification(self) -> None:
        """Send a notification for the start of a long break"""
        self.notification.title = "Pomodoro Timer"
        self.notification.message = f"🌴 Long break started!"

        self.notification.send()
