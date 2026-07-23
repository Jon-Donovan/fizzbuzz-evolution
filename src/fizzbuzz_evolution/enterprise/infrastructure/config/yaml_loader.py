"""YAML-backed Enterprise configuration loader."""

from collections.abc import Mapping
from pathlib import Path
from typing import cast

import yaml  # type: ignore[import-untyped]

from ...domain import InvalidRangeError, NumberRange
from .errors import (
    ConfigurationFileNotFoundError,
    ConfigurationSchemaError,
    ConfigurationSyntaxError,
    UnsupportedConfigurationVersionError,
    UnsupportedRuleTypeError,
)
from .models import (
    ApplicationConfig,
    DivisibilityRuleConfig,
    EnterpriseConfig,
    LoggingConfig,
    LogLevel,
    OutputFormat,
)

SUPPORTED_VERSION = 1


class YamlConfigLoader:
    """Load and validate Enterprise application configuration from YAML."""

    def load(self, path: Path) -> EnterpriseConfig:
        """Load a YAML configuration file."""
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError as error:
            raise ConfigurationFileNotFoundError(path) from error
        try:
            raw: object = yaml.safe_load(text)
        except yaml.YAMLError as error:
            raise ConfigurationSyntaxError(path, str(error)) from error
        return self.parse(raw)

    def parse(self, raw: object) -> EnterpriseConfig:
        """Validate an already parsed YAML value."""
        root = _mapping(raw, "Configuration root must be a mapping.")
        version = _integer(_required(root, "version", "configuration"), "version")
        if version != SUPPORTED_VERSION:
            raise UnsupportedConfigurationVersionError(version)

        application_raw = _optional_mapping(root, "application")
        default_start = _optional_integer(application_raw, "default_start", 1)
        default_end = _optional_integer(application_raw, "default_end", 100)
        try:
            NumberRange(default_start, default_end)
        except InvalidRangeError as error:
            raise ConfigurationSchemaError(str(error)) from error
        output_format = _output_format(
            application_raw.get("output_format", OutputFormat.TEXT.value),
            "application.output_format",
        )

        logging_raw = _optional_mapping(root, "logging")
        log_level = _log_level(
            logging_raw.get("level", LogLevel.WARNING.value),
            "logging.level",
        )

        rules_raw = _required(root, "rules", "configuration")
        if not isinstance(rules_raw, list):
            raise ConfigurationSchemaError("configuration.rules must be a list.")
        rules = tuple(_parse_rule(item, index) for index, item in enumerate(rules_raw))

        return EnterpriseConfig(
            version=version,
            application=ApplicationConfig(default_start, default_end, output_format),
            logging=LoggingConfig(log_level),
            rules=rules,
        )


def _parse_rule(raw: object, index: int) -> DivisibilityRuleConfig:
    context = f"rules[{index}]"
    item = _mapping(raw, f"{context} must be a mapping.")
    rule_type = _string(_required(item, "type", context), f"{context}.type")
    if rule_type != "divisibility":
        raise UnsupportedRuleTypeError(rule_type)
    return DivisibilityRuleConfig(
        rule_id=_string(_required(item, "id", context), f"{context}.id"),
        divisor=_integer(_required(item, "divisor", context), f"{context}.divisor"),
        replacement=_string(
            _required(item, "replacement", context),
            f"{context}.replacement",
        ),
    )


def _mapping(raw: object, message: str) -> Mapping[str, object]:
    if not isinstance(raw, Mapping) or not all(isinstance(key, str) for key in raw):
        raise ConfigurationSchemaError(message)
    return cast(Mapping[str, object], raw)


def _optional_mapping(parent: Mapping[str, object], key: str) -> Mapping[str, object]:
    raw = parent.get(key, {})
    return _mapping(raw, f"configuration.{key} must be a mapping.")


def _required(parent: Mapping[str, object], key: str, context: str) -> object:
    if key not in parent:
        raise ConfigurationSchemaError(f"Missing required field: {context}.{key}")
    return parent[key]


def _integer(raw: object, field: str) -> int:
    if not isinstance(raw, int) or isinstance(raw, bool):
        raise ConfigurationSchemaError(f"{field} must be an integer.")
    return raw


def _optional_integer(parent: Mapping[str, object], key: str, default: int) -> int:
    return _integer(parent.get(key, default), f"application.{key}")


def _string(raw: object, field: str) -> str:
    if not isinstance(raw, str):
        raise ConfigurationSchemaError(f"{field} must be a string.")
    return raw


def _output_format(raw: object, field: str) -> OutputFormat:
    value = _string(raw, field).lower()
    try:
        return OutputFormat(value)
    except ValueError as error:
        choices = ", ".join(item.value for item in OutputFormat)
        raise ConfigurationSchemaError(f"{field} must be one of: {choices}.") from error


def _log_level(raw: object, field: str) -> LogLevel:
    value = _string(raw, field).upper()
    try:
        return LogLevel(value)
    except ValueError as error:
        choices = ", ".join(item.value for item in LogLevel)
        raise ConfigurationSchemaError(f"{field} must be one of: {choices}.") from error
