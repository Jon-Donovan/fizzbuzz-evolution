"""Tests for stage command-line entry points."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src"


@pytest.mark.parametrize("stage", ["classic", "literal"])
def test_stage_module_prints_fizzbuzz_sequence(stage: str) -> None:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(SOURCE_ROOT)

    completed = subprocess.run(
        [sys.executable, "-m", f"fizzbuzz_evolution.{stage}"],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )

    lines = completed.stdout.splitlines()

    assert len(lines) == 100
    assert lines[:5] == ["1", "2", "Fizz", "4", "Buzz"]
    assert lines[14] == "FizzBuzz"
    assert lines[-1] == "Buzz"
