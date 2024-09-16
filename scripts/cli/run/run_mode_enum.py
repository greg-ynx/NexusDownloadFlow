"""Enum containing the mode choices."""
from enum import StrEnum, auto


class RunModeEnum(StrEnum):
    """Enumeration representing the different execution modes available."""

    CLASSIC: auto = auto()
    """Classic execution mode with default parameters."""

    CUSTOM: auto = auto()
    """Custom execution mode with specific parameters."""

    HYBRID: auto = auto()
    """Hybrid mode combining classic and custom parameters."""
