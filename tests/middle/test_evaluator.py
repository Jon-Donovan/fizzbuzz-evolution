"""Tests for Middle-stage value evaluation."""

import pytest

from fizzbuzz_evolution.middle import evaluate


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (1, "1"),
        (2, "2"),
        (3, "Fizz"),
        (5, "Buzz"),
        (6, "Fizz"),
        (10, "Buzz"),
        (15, "FizzBuzz"),
        (30, "FizzBuzz"),
        (0, "FizzBuzz"),
        (-1, "-1"),
        (-3, "Fizz"),
        (-5, "Buzz"),
        (-15, "FizzBuzz"),
    ],
)
def test_evaluate(number: int, expected: str) -> None:
    assert evaluate(number) == expected
