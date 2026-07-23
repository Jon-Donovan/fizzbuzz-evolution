"""Presentation-layer exit codes."""

from enum import IntEnum


class ExitCode(IntEnum):
    """Stable process exit codes exposed by the Enterprise CLI."""

    SUCCESS = 0
    INTERNAL_ERROR = 1
    ARGUMENT_ERROR = 2
    CONFIGURATION_ERROR = 3
    DOMAIN_ERROR = 4
