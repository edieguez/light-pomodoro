"""Models for the Pomodoro application"""
from pydantic import BaseModel, Field


class SmartBulbConfig(BaseModel):
    """Model representing a smart bulb configuration."""
    device_id: str
    address: str
    local_key: str
    version: float

class Break(BaseModel):
    """Model representing a break period in a Pomodoro timer."""
    duration: int
    color: list[int]
    brightness: int


class PomodoroConfig(BaseModel):
    """Model representing a Pomodoro timer configuration."""
    duration: int
    color: list[int]
    brightness: int
    short_break: Break
    long_break: Break
    cycles_before_long_break: int
