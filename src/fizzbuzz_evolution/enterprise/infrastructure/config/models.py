"""Typed configuration models for the Enterprise application."""

from dataclasses import dataclass
from enum import StrEnum


class OutputFormat(StrEnum):
    """Supported presentation formats."""

    TEXT = "text"
    JSON = "json"


class LogLevel(StrEnum):
    """Supported application log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True, slots=True)
class ApplicationConfig:
    """Default application settings loaded from configuration."""

    default_start: int = 1
    default_end: int = 100
    output_format: OutputFormat = OutputFormat.TEXT


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    """Logging settings loaded from configuration."""

    level: LogLevel = LogLevel.WARNING


@dataclass(frozen=True, slots=True)
class DivisibilityRuleConfig:
    """Configuration data for one divisibility rule."""

    rule_id: str
    divisor: int
    replacement: str


@dataclass(frozen=True, slots=True)
class EnterpriseConfig:
    """Complete validated Enterprise application configuration."""

    version: int
    application: ApplicationConfig
    logging: LoggingConfig
    rules: tuple[DivisibilityRuleConfig, ...]
