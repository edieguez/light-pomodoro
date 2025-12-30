"""Module for sending notifications for Pomodoro timer events"""
import os

from notifypy import Notify
from tinytuya import BulbDevice

import util.payload as payload_utils
from pomodoro.models import SmartBulbConfig, ThemeConfig, PhaseColor


class SmartBulbNotifier:
    """Class for sending notifications via smart bulb"""

    def __init__(self, smart_bulb_config: SmartBulbConfig, theme_config: ThemeConfig) -> None:
        self.smart_bulb: BulbDevice = BulbDevice(
            dev_id=smart_bulb_config.device_id,
            address=smart_bulb_config.address,
            local_key=smart_bulb_config.local_key,
            version=smart_bulb_config.version,
        )
        self.theme_config = theme_config

    def work_notification(self) -> None:
        """Set bulb color for work session"""
        self._set_dps_payload(self.theme_config.work)

    def short_break_notification(self) -> None:
        """Set bulb color for short break"""
        self._set_dps_payload(self.theme_config.short_break)

    def long_break_notification(self) -> None:
        """Set bulb color for long break"""
        self._set_dps_payload(self.theme_config.long_break)

    def turn_off(self) -> None:
        """Turn off the smart bulb"""
        self.smart_bulb.set_status(False, 20)

    def _set_dps_payload(self, phase_color: PhaseColor) -> None:
        payload: dict[str, object] = payload_utils.generate_payload(phase_color)

        self.smart_bulb.set_multiple_values(payload)


class NoOpBulbNotifier:
    """A SmartBulbNotifier that does nothing (for no-bulb scenarios)"""

    def work_notification(self) -> None:
        """Do nothing for work notification"""

    def short_break_notification(self) -> None:
        """Do nothing for short break notification"""

    def long_break_notification(self) -> None:
        """Do nothing for long break notification"""

    def turn_off(self) -> None:
        """Do nothing for turning off the bulb"""


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
        self.notification.message = "🍅 Work session started!"

        self.notification.send()

    def short_break_notification(self) -> None:
        """Send a notification for the start of a short break"""
        self.notification.title = "Pomodoro Timer"
        self.notification.message = "☕️ Short break started!"

        self.notification.send()

    def long_break_notification(self) -> None:
        """Send a notification for the start of a long break"""
        self.notification.title = "Pomodoro Timer"
        self.notification.message = "🌴 Long break started!"

        self.notification.send()


class NoOpDesktopNotifier:
    """A DesktopNotifier that does nothing (for no-desktop-notification scenarios)"""

    def work_notification(self) -> None:
        """Do nothing for work notification"""

    def short_break_notification(self) -> None:
        """Do nothing for short break notification"""

    def long_break_notification(self) -> None:
        """Do nothing for long break notification"""
