"""Command-line interface for Enterprise FizzBuzz."""

import argparse
import logging
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Never, TextIO

from ..application import GenerateSequenceCommand
from ..bootstrap import EnterpriseApplication, create_application
from ..domain import DomainError
from ..infrastructure.config import (
    ApplicationConfig,
    ConfigurationError,
    DivisibilityRuleConfig,
    EnterpriseConfig,
    LoggingConfig,
    LogLevel,
    OutputFormat,
    YamlConfigLoader,
)
from ..infrastructure.logging import configure_logging
from .errors import ExitCode
from .presenters import create_presenter

_LOGGER = logging.getLogger("fizzbuzz_evolution.enterprise")


class ArgumentParser(argparse.ArgumentParser):
    """Argument parser that raises instead of terminating the process."""

    def error(self, message: str) -> Never:
        """Raise a controlled argument error."""
        raise ValueError(message)


def build_parser() -> ArgumentParser:
    """Build the Enterprise command-line parser."""
    parser = ArgumentParser(description="Run the Enterprise FizzBuzz application.")
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--format", choices=[item.value for item in OutputFormat])
    parser.add_argument("--log-level", choices=[item.value for item in LogLevel])
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Run the Enterprise CLI and return a stable process exit code."""
    output = stdout if stdout is not None else sys.stdout
    errors = stderr if stderr is not None else sys.stderr
    try:
        arguments = build_parser().parse_args(argv)
    except ValueError as error:
        print(f"error: {error}", file=errors)
        return ExitCode.ARGUMENT_ERROR

    try:
        config = _load_config(arguments.config)
        level = LogLevel(arguments.log_level) if arguments.log_level else config.logging.level
        configure_logging(level, errors)
        application = create_application(config)
        start = arguments.start if arguments.start is not None else config.application.default_start
        end = arguments.end if arguments.end is not None else config.application.default_end
        output_format = (
            OutputFormat(arguments.format)
            if arguments.format is not None
            else config.application.output_format
        )
        _log_start(application, start, end, output_format, arguments.config)
        result = application.use_case.execute(GenerateSequenceCommand(start=start, end=end))
        rendered = create_presenter(output_format).present(result)
        print(rendered, file=output)
        _LOGGER.info("application_completed items=%d", len(result.items))
        return ExitCode.SUCCESS
    except ConfigurationError as error:
        print(f"error: {error}", file=errors)
        return ExitCode.CONFIGURATION_ERROR
    except DomainError as error:
        _LOGGER.error("domain_error detail=%s", error)
        print(f"error: {error}", file=errors)
        return ExitCode.DOMAIN_ERROR
    except Exception as error:  # pragma: no cover - defensive process boundary
        _LOGGER.exception("unexpected_error")
        print(f"error: unexpected internal failure: {error}", file=errors)
        return ExitCode.INTERNAL_ERROR


def _load_config(path: Path | None) -> EnterpriseConfig:
    if path is not None:
        return YamlConfigLoader().load(path)
    return EnterpriseConfig(
        version=1,
        application=ApplicationConfig(),
        logging=LoggingConfig(),
        rules=(
            DivisibilityRuleConfig("fizz", 3, "Fizz"),
            DivisibilityRuleConfig("buzz", 5, "Buzz"),
        ),
    )


def _log_start(
    application: EnterpriseApplication,
    start: int,
    end: int,
    output_format: OutputFormat,
    config_path: Path | None,
) -> None:
    source = str(config_path) if config_path is not None else "built-in"
    _LOGGER.info(
        "application_started source=%s start=%d end=%d format=%s rules=%d",
        source,
        start,
        end,
        output_format.value,
        len(application.config.rules),
    )
    _LOGGER.debug(
        "configured_rule_ids=%s",
        [rule.rule_id for rule in application.config.rules],
    )
