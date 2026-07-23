"""Tests for YAML Enterprise configuration loading."""

from pathlib import Path

import pytest

from fizzbuzz_evolution.enterprise.infrastructure.config import (
    ConfigurationFileNotFoundError,
    ConfigurationSchemaError,
    ConfigurationSyntaxError,
    LogLevel,
    OutputFormat,
    UnsupportedConfigurationVersionError,
    UnsupportedRuleTypeError,
    YamlConfigLoader,
)


def test_loads_complete_configuration(tmp_path: Path) -> None:
    path = tmp_path / "config.yml"
    path.write_text(
        """
version: 1
application:
  default_start: -5
  default_end: 105
  output_format: json
logging:
  level: debug
rules:
  - id: fizz
    type: divisibility
    divisor: 3
    replacement: Fizz
  - id: bazz
    type: divisibility
    divisor: 7
    replacement: Bazz
""",
        encoding="utf-8",
    )

    config = YamlConfigLoader().load(path)

    assert config.application.default_start == -5
    assert config.application.default_end == 105
    assert config.application.output_format is OutputFormat.JSON
    assert config.logging.level is LogLevel.DEBUG
    assert [rule.rule_id for rule in config.rules] == ["fizz", "bazz"]


def test_applies_optional_defaults() -> None:
    config = YamlConfigLoader().parse(
        {
            "version": 1,
            "rules": [],
        }
    )

    assert config.application.default_start == 1
    assert config.application.default_end == 100
    assert config.application.output_format is OutputFormat.TEXT
    assert config.logging.level is LogLevel.WARNING


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        (None, "root"),
        ({"version": "1", "rules": []}, "version must be an integer"),
        ({"version": 1}, "Missing required field"),
        ({"version": 1, "rules": {}}, "must be a list"),
        ({"version": 1, "rules": ["bad"]}, "must be a mapping"),
        ({"version": 1, "rules": [{"type": "divisibility"}]}, "Missing required field"),
        (
            {
                "version": 1,
                "application": {"output_format": "xml"},
                "rules": [],
            },
            "output_format",
        ),
        (
            {"version": 1, "logging": {"level": "TRACE"}, "rules": []},
            "logging.level",
        ),
        (
            {
                "version": 1,
                "application": {"default_start": 2, "default_end": 1},
                "rules": [],
            },
            "Range start",
        ),
    ],
)
def test_rejects_invalid_schema(raw: object, message: str) -> None:
    with pytest.raises(ConfigurationSchemaError, match=message):
        YamlConfigLoader().parse(raw)


def test_rejects_unsupported_version() -> None:
    with pytest.raises(UnsupportedConfigurationVersionError):
        YamlConfigLoader().parse({"version": 2, "rules": []})


def test_rejects_unsupported_rule_type() -> None:
    with pytest.raises(UnsupportedRuleTypeError):
        YamlConfigLoader().parse(
            {
                "version": 1,
                "rules": [
                    {
                        "id": "exact",
                        "type": "exact",
                        "divisor": 1,
                        "replacement": "One",
                    }
                ],
            }
        )


def test_reports_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.yml"

    with pytest.raises(ConfigurationFileNotFoundError) as raised:
        YamlConfigLoader().load(missing)

    assert raised.value.path == missing


def test_reports_invalid_yaml(tmp_path: Path) -> None:
    path = tmp_path / "broken.yml"
    path.write_text("rules: [", encoding="utf-8")

    with pytest.raises(ConfigurationSyntaxError):
        YamlConfigLoader().load(path)
