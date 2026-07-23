"""Shared behavioral contract for every implemented FizzBuzz stage."""

from collections.abc import Callable

import pytest

from fizzbuzz_evolution.classic import (
    fizzbuzz as classic_fizzbuzz,
)
from fizzbuzz_evolution.classic import (
    generate_fizzbuzz as classic_generate,
)
from fizzbuzz_evolution.enterprise import (
    GenerateSequenceCommand,
    create_fizzbuzz_use_case,
)
from fizzbuzz_evolution.enterprise.domain import InvalidRangeError as EnterpriseInvalidRangeError
from fizzbuzz_evolution.literal import (
    fizzbuzz as literal_fizzbuzz,
)
from fizzbuzz_evolution.literal import (
    generate_fizzbuzz as literal_generate,
)
from fizzbuzz_evolution.middle import evaluate as middle_evaluate
from fizzbuzz_evolution.middle import generate as middle_generate
from fizzbuzz_evolution.middle.errors import InvalidRangeError as MiddleInvalidRangeError
from fizzbuzz_evolution.senior import create_fizzbuzz_engine
from fizzbuzz_evolution.senior import generate as senior_generate
from fizzbuzz_evolution.senior.errors import InvalidRangeError as SeniorInvalidRangeError

FizzBuzzFunction = Callable[[int], str]
SequenceFunction = Callable[[int, int], list[str]]
SENIOR_ENGINE = create_fizzbuzz_engine()
ENTERPRISE_USE_CASE = create_fizzbuzz_use_case()


def enterprise_evaluate(number: int) -> str:
    """Adapt the structured Enterprise result to the shared string contract."""
    result = ENTERPRISE_USE_CASE.execute(GenerateSequenceCommand(number, number))
    return result.items[0].value


def senior_generate_adapter(start: int, end: int) -> list[str]:
    """Adapt the engine-aware Senior generator to the shared sequence contract."""
    return senior_generate(SENIOR_ENGINE, start, end)


def enterprise_generate(start: int, end: int) -> list[str]:
    """Adapt the Enterprise use case to the shared sequence contract."""
    result = ENTERPRISE_USE_CASE.execute(GenerateSequenceCommand(start, end))
    return [item.value for item in result.items]


EVALUATORS: tuple[FizzBuzzFunction, ...] = (
    classic_fizzbuzz,
    literal_fizzbuzz,
    middle_evaluate,
    SENIOR_ENGINE.evaluate,
    enterprise_evaluate,
)

GENERATORS: tuple[SequenceFunction, ...] = (
    classic_generate,
    literal_generate,
    middle_generate,
    senior_generate_adapter,
    enterprise_generate,
)


@pytest.mark.parametrize("implementation", EVALUATORS)
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
def test_evaluation_contract(
    implementation: FizzBuzzFunction,
    number: int,
    expected: str,
) -> None:
    assert implementation(number) == expected


@pytest.mark.parametrize("implementation", GENERATORS)
def test_sequence_contract(implementation: SequenceFunction) -> None:
    assert implementation(-1, 5) == ["-1", "FizzBuzz", "1", "2", "Fizz", "4", "Buzz"]


@pytest.mark.parametrize("implementation", GENERATORS)
def test_single_value_range_contract(implementation: SequenceFunction) -> None:
    assert implementation(15, 15) == ["FizzBuzz"]


@pytest.mark.parametrize(
    ("implementation", "expected_error"),
    [
        (middle_generate, MiddleInvalidRangeError),
        (senior_generate_adapter, SeniorInvalidRangeError),
        (enterprise_generate, EnterpriseInvalidRangeError),
    ],
)
def test_validated_stage_reversed_range_contract(
    implementation: SequenceFunction,
    expected_error: type[Exception],
) -> None:
    with pytest.raises(expected_error):
        implementation(2, 1)
