"""Tests for the Enterprise command-line adapter."""

import io
import json
from pathlib import Path

from fizzbuzz_evolution.enterprise.presentation.cli import main
from fizzbuzz_evolution.enterprise.presentation.errors import ExitCode


def test_runs_with_builtin_defaults_and_custom_range() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()

    code = main(["--start", "14", "--end", "16"], stdout=stdout, stderr=stderr)

    assert code == ExitCode.SUCCESS
    assert stdout.getvalue() == "14\nFizzBuzz\n16\n"
    assert stderr.getvalue() == ""


def test_renders_json_without_mixing_logs_into_stdout() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()

    code = main(
        ["--start", "3", "--end", "3", "--format", "json", "--log-level", "INFO"],
        stdout=stdout,
        stderr=stderr,
    )

    payload = json.loads(stdout.getvalue())
    assert code == ExitCode.SUCCESS
    assert payload["items"][0]["value"] == "Fizz"
    assert "application_started" in stderr.getvalue()
    assert "application_completed" in stderr.getvalue()


def test_cli_arguments_override_yaml_defaults(tmp_path: Path) -> None:
    config = tmp_path / "config.yml"
    config.write_text(
        """
version: 1
application:
  default_start: 1
  default_end: 105
  output_format: json
logging:
  level: WARNING
rules:
  - id: bazz
    type: divisibility
    divisor: 7
    replacement: Bazz
""",
        encoding="utf-8",
    )
    stdout = io.StringIO()
    stderr = io.StringIO()

    code = main(
        ["--config", str(config), "--start", "14", "--end", "14", "--format", "text"],
        stdout=stdout,
        stderr=stderr,
    )

    assert code == ExitCode.SUCCESS
    assert stdout.getvalue() == "Bazz\n"
    assert stderr.getvalue() == ""


def test_reports_configuration_error_without_traceback(tmp_path: Path) -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()

    code = main(
        ["--config", str(tmp_path / "missing.yml")],
        stdout=stdout,
        stderr=stderr,
    )

    assert code == ExitCode.CONFIGURATION_ERROR
    assert stdout.getvalue() == ""
    assert "Configuration file not found" in stderr.getvalue()
    assert "Traceback" not in stderr.getvalue()


def test_reports_domain_error_without_output() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()

    code = main(["--start", "10", "--end", "1"], stdout=stdout, stderr=stderr)

    assert code == ExitCode.DOMAIN_ERROR
    assert stdout.getvalue() == ""
    assert "Range start" in stderr.getvalue()
    assert "Traceback" not in stderr.getvalue()


def test_reports_argument_error() -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()

    code = main(["--format", "xml"], stdout=stdout, stderr=stderr)

    assert code == ExitCode.ARGUMENT_ERROR
    assert stdout.getvalue() == ""
    assert "invalid choice" in stderr.getvalue()
