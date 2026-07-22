"""Tests for the Middle-stage command-line interface."""

import pytest

from fizzbuzz_evolution.middle.cli import main


def test_main_prints_requested_range(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--start", "3", "--end", "5"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Fizz\n4\nBuzz\n"
    assert captured.err == ""


def test_main_reports_invalid_range_to_stderr(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main(["--start", "5", "--end", "3"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert captured.out == ""
    assert captured.err == ("error: range start (5) must not be greater than range end (3)\n")
