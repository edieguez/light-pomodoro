"""Models for the Pomodoro application"""

from pydantic import BaseModel, Field, field_validator
from typing import List


class SmartBulbConfig(BaseModel):
    """Model representing a smart bulb configuration."""
    device_id: str
    address: str
    local_key: str
    version: float = Field(..., ge=3.1, le=3.5)


class Break(BaseModel):
    """Model representing a break period in a Pomodoro timer."""
    duration: int = Field(..., gt=0, description="Duration in minutes")
    color: List[int] = Field(..., description="RGB color [0–255, 0–255, 0–255]")
    brightness: int = Field(..., ge=0, le=1000)

    @field_validator("color")
    @classmethod
    def validate_rgb(cls, value):
        if len(value) != 3:
            raise ValueError("RGB color must have exactly 3 values")

        for channel in value:
            if not isinstance(channel, int):
                raise ValueError("RGB values must be integers")
            if not 0 <= channel <= 255:
                raise ValueError("RGB values must be between 0 and 255")

        return value


class PomodoroConfig(BaseModel):
    """Model representing a Pomodoro timer configuration."""
    duration: int = Field(..., gt=0, description="Work duration in minutes")
    color: List[int] = Field(..., description="RGB color [0-255, 0-255, 0-255]")
    saturation: int = Field(..., ge=0, le=1000)
    brightness: int = Field(..., ge=10, le=1000)
    short_break: Break
    long_break: Break
    cycles_before_long_break: int = Field(..., gt=0)

    @field_validator("color")
    def validate_rgb(cls, value):
        if len(value) != 3:
            raise ValueError("RGB color must have exactly 3 values")

        for channel in value:
            if not isinstance(channel, int):
                raise ValueError("RGB values must be integers")
            if not 0 <= channel <= 255:
                raise ValueError("RGB values must be between 0 and 255")

        return value
