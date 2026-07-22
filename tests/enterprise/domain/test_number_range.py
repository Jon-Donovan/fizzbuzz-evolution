"""Tests for Enterprise number range models."""

from dataclasses import FrozenInstanceError

import pytest

from fizzbuzz_evolution.enterprise import InvalidRangeError, Number, NumberRange


def test_number_range_is_inclusive() -> None:
    assert tuple(NumberRange(-1, 1)) == (Number(-1), Number(0), Number(1))


def test_number_range_accepts_one_value() -> None:
    assert tuple(NumberRange(3, 3)) == (Number(3),)


def test_number_range_rejects_reversed_bounds() -> None:
    with pytest.raises(InvalidRangeError) as error:
        NumberRange(10, 1)

    assert error.value.start == 10
    assert error.value.end == 1
    assert str(error.value) == "Range start (10) must not be greater than end (1)."


def test_number_is_immutable() -> None:
    number = Number(1)

    with pytest.raises(FrozenInstanceError):
        number.value = 2  # type: ignore[misc]
