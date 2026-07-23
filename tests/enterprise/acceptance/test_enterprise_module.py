"""Acceptance tests for the installed-style Enterprise module entry point."""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    source_path = str(ROOT / "src")
    environment["PYTHONPATH"] = os.pathsep.join(
        filter(None, (source_path, environment.get("PYTHONPATH", "")))
    )
    return subprocess.run(
        [sys.executable, "-m", "fizzbuzz_evolution.enterprise", *arguments],
        cwd=ROOT,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )


def test_module_outputs_text_sequence() -> None:
    completed = _run("--start", "14", "--end", "16")

    assert completed.returncode == 0
    assert completed.stdout == "14\nFizzBuzz\n16\n"
    assert "Traceback" not in completed.stderr


def test_module_outputs_valid_json() -> None:
    completed = _run("--start", "3", "--end", "5", "--format", "json")

    payload = json.loads(completed.stdout)
    assert completed.returncode == 0
    assert payload["items"][0]["matches"][0]["rule_id"] == "fizz"
    assert "Traceback" not in completed.stderr


def test_module_reports_invalid_range() -> None:
    completed = _run("--start", "2", "--end", "1")

    assert completed.returncode == 4
    assert completed.stdout == ""
    assert "Range start" in completed.stderr
    assert "Traceback" not in completed.stderr
