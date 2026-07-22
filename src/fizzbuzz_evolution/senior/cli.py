"""Command-line interface for the Senior-stage implementation."""

import argparse
import sys
from collections.abc import Sequence

from .errors import InvalidRangeError
from .generator import generate
from .presets import create_fizzbuzz_engine


def build_parser() -> argparse.ArgumentParser:
    """Create the Senior-stage argument parser."""
    parser = argparse.ArgumentParser(
        prog="python -m fizzbuzz_evolution.senior",
        description="Print an inclusive sequence using the classic FizzBuzz rule preset.",
    )
    parser.add_argument("--start", type=int, default=1, help="first number (default: 1)")
    parser.add_argument("--end", type=int, default=100, help="last number (default: 100)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    arguments = build_parser().parse_args(argv)
    engine = create_fizzbuzz_engine()

    try:
        values = generate(engine, arguments.start, arguments.end)
    except InvalidRangeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(*values, sep="\n")
    return 0
