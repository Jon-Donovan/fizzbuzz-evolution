"""Shared behavioral contract for implemented FizzBuzz stages."""

from collections.abc import Callable

import pytest

from fizzbuzz_evolution.classic import fizzbuzz as classic_fizzbuzz
from fizzbuzz_evolution.literal import fizzbuzz as literal_fizzbuzz

FizzBuzzFunction = Callable[[int], str]


@pytest.mark.parametrize("implementation", [classic_fizzbuzz, literal_fizzbuzz])
@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (1, "1"),
        (3, "Fizz"),
        (5, "Buzz"),
        (15, "FizzBuzz"),
    ],
)
def test_stage_contract(
    implementation: FizzBuzzFunction,
    number: int,
    expected: str,
) -> None:
    assert implementation(number) == expected
