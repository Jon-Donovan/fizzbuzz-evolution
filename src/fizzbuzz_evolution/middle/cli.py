"""Command-line interface for the Middle-stage implementation."""

import argparse
import sys
from collections.abc import Sequence

from .errors import InvalidRangeError
from .generator import generate


def build_parser() -> argparse.ArgumentParser:
    """Create the Middle-stage argument parser."""
    parser = argparse.ArgumentParser(
        prog="python -m fizzbuzz_evolution.middle",
        description="Print an inclusive FizzBuzz sequence.",
    )
    parser.add_argument("--start", type=int, default=1, help="first number (default: 1)")
    parser.add_argument("--end", type=int, default=100, help="last number (default: 100)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    arguments = build_parser().parse_args(argv)

    try:
        values = generate(arguments.start, arguments.end)
    except InvalidRangeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(*values, sep="\n")
    return 0
