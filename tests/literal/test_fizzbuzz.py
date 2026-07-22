"""Tests for the literal FizzBuzz implementation."""

import pytest

from fizzbuzz_evolution.literal import fizzbuzz, generate_fizzbuzz


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
        (-3, "Fizz"),
        (-5, "Buzz"),
        (-15, "FizzBuzz"),
    ],
)
def test_fizzbuzz(number: int, expected: str) -> None:
    assert fizzbuzz(number) == expected


def test_generate_fizzbuzz_uses_inclusive_bounds() -> None:
    assert generate_fizzbuzz(3, 5) == ["Fizz", "4", "Buzz"]


def test_generate_default_range_contains_one_hundred_values() -> None:
    values = generate_fizzbuzz()

    assert len(values) == 100
    assert values[0] == "1"
    assert values[-1] == "Buzz"
