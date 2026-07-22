"""Tests for Senior-stage range generation."""

import pytest

from fizzbuzz_evolution.senior import InvalidRangeError, create_fizzbuzz_engine, generate


def test_generate_uses_engine_for_inclusive_range() -> None:
    assert generate(create_fizzbuzz_engine(), 3, 5) == ["Fizz", "4", "Buzz"]


def test_generate_supports_single_value_and_negative_range() -> None:
    engine = create_fizzbuzz_engine()

    assert generate(engine, 3, 3) == ["Fizz"]
    assert generate(engine, -1, 1) == ["-1", "FizzBuzz", "1"]


def test_generate_uses_default_bounds() -> None:
    values = generate(create_fizzbuzz_engine())

    assert len(values) == 100
    assert values[:5] == ["1", "2", "Fizz", "4", "Buzz"]
    assert values[-1] == "Buzz"


def test_generate_rejects_reversed_range() -> None:
    with pytest.raises(InvalidRangeError) as error_info:
        generate(create_fizzbuzz_engine(), 5, 3)

    assert error_info.value.start == 5
    assert error_info.value.end == 3
