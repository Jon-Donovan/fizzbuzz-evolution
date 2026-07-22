"""Shared behavioral contract for implemented FizzBuzz stages."""

from collections.abc import Callable

import pytest

from fizzbuzz_evolution.classic import fizzbuzz as classic_fizzbuzz
from fizzbuzz_evolution.literal import fizzbuzz as literal_fizzbuzz
from fizzbuzz_evolution.middle import evaluate as middle_evaluate
from fizzbuzz_evolution.senior import create_fizzbuzz_engine

FizzBuzzFunction = Callable[[int], str]
SENIOR_EVALUATE = create_fizzbuzz_engine().evaluate


@pytest.mark.parametrize(
    "implementation", [classic_fizzbuzz, literal_fizzbuzz, middle_evaluate, SENIOR_EVALUATE]
)
@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (1, "1"),
        (3, "Fizz"),
        (5, "Buzz"),
        (15, "FizzBuzz"),
        (0, "FizzBuzz"),
        (-3, "Fizz"),
        (-5, "Buzz"),
        (-15, "FizzBuzz"),
    ],
)
def test_stage_contract(
    implementation: FizzBuzzFunction,
    number: int,
    expected: str,
) -> None:
    assert implementation(number) == expected
