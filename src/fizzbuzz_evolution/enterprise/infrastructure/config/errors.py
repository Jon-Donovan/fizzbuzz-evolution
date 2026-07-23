"""Configuration errors exposed by the infrastructure layer."""

from pathlib import Path


class ConfigurationError(Exception):
    """Base class for expected configuration failures."""


class ConfigurationFileNotFoundError(ConfigurationError):
    """Raised when a requested configuration file does not exist."""

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(f"Configuration file not found: {path}")


class ConfigurationSyntaxError(ConfigurationError):
    """Raised when YAML cannot be parsed."""

    def __init__(self, path: Path, detail: str) -> None:
        self.path = path
        self.detail = detail
        super().__init__(f"Invalid YAML in configuration file {path}: {detail}")


class ConfigurationSchemaError(ConfigurationError):
    """Raised when parsed configuration does not match the expected schema."""


class UnsupportedConfigurationVersionError(ConfigurationError):
    """Raised when a configuration version is not supported."""

    def __init__(self, version: int) -> None:
        self.version = version
        super().__init__(f"Unsupported configuration version: {version}")


class UnsupportedRuleTypeError(ConfigurationError):
    """Raised when configuration declares an unknown rule type."""

    def __init__(self, rule_type: str) -> None:
        self.rule_type = rule_type
        super().__init__(f"Unsupported rule type: {rule_type}")
