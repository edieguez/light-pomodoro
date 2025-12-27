"""Models for the Pomodoro application"""

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class SmartBulbConfig(BaseModel):
    """Model representing a smart bulb configuration."""
    name: str = Field(..., min_length=1, max_length=32)
    device_id: str
    address: str
    local_key: str
    version: float = Field(..., ge=3.1, le=3.5)


class PomodoroConfig(BaseModel):
    """Model representing a Pomodoro timer configuration."""
    name: str = Field(..., min_length=1, max_length=32)
    duration: int = Field(..., gt=0, description="Work duration in minutes")
    short_break: int = Field(..., gt=0, description="Short break duration in minutes")
    long_break: int = Field(..., gt=0, description="Long break duration in minutes")
    cycles_before_long_break: int = Field(..., gt=0)


class ThemeColor(BaseModel):
    """Model representing a color in a theme configuration."""
    color: List[int] = Field(..., description="RGB color [0-255, 0-255, 0-255]")
    saturation: int = Field(..., ge=10, le=1000)
    brightness: int = Field(..., ge=10, le=1000)
    dps: Optional[str] = Field("", description="Optional DPS string for custom payload")

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


class ThemeConfig(BaseModel):
    """Model representing a theme configuration for smart bulb colors."""
    name: str = Field(..., min_length=1, max_length=32)
    work: ThemeColor
    short_break: ThemeColor
    long_break: ThemeColor
