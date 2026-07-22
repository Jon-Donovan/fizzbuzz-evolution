"""Tests for the Middle-stage exception hierarchy."""

from fizzbuzz_evolution.middle import FizzBuzzError, InvalidRangeError


def test_invalid_range_error_is_a_fizzbuzz_error() -> None:
    error = InvalidRangeError(5, 4)

    assert isinstance(error, FizzBuzzError)
