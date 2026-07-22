"""Tests for Middle-stage sequence generation."""

import pytest

from fizzbuzz_evolution.middle import InvalidRangeError, generate


def test_generate_uses_inclusive_bounds() -> None:
    assert generate(3, 5) == ["Fizz", "4", "Buzz"]


def test_generate_accepts_a_single_value_range() -> None:
    assert generate(3, 3) == ["Fizz"]


def test_generate_supports_a_range_crossing_zero() -> None:
    assert generate(-1, 1) == ["-1", "FizzBuzz", "1"]


def test_generate_supports_negative_bounds() -> None:
    assert generate(-5, -3) == ["Buzz", "-4", "Fizz"]


def test_generate_default_range_contains_one_hundred_values() -> None:
    values = generate()

    assert len(values) == 100
    assert values[0] == "1"
    assert values[-1] == "Buzz"


def test_generate_rejects_a_reversed_range() -> None:
    with pytest.raises(InvalidRangeError) as captured:
        generate(10, 1)

    assert captured.value.start == 10
    assert captured.value.end == 1
    assert str(captured.value) == "range start (10) must not be greater than range end (1)"
