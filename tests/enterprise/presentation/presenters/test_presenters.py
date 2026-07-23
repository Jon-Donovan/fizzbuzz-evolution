"""Tests for Enterprise text and JSON presenters."""

import json

from fizzbuzz_evolution.enterprise import (
    GenerateSequenceCommand,
    GenerateSequenceResult,
    create_fizzbuzz_use_case,
)
from fizzbuzz_evolution.enterprise.infrastructure.config import OutputFormat
from fizzbuzz_evolution.enterprise.presentation.presenters import (
    JsonPresenter,
    TextPresenter,
    create_presenter,
)


def _result() -> GenerateSequenceResult:
    return create_fizzbuzz_use_case().execute(GenerateSequenceCommand(3, 5))


def test_text_presenter_renders_one_value_per_line() -> None:
    assert TextPresenter().present(_result()) == "Fizz\n4\nBuzz"


def test_json_presenter_exposes_structured_matches() -> None:
    payload = json.loads(JsonPresenter().present(_result()))

    assert payload["start"] == 3
    assert payload["end"] == 5
    assert payload["items"][0] == {
        "number": 3,
        "value": "Fizz",
        "matches": [{"rule_id": "fizz", "value": "Fizz"}],
    }
    assert payload["items"][1]["matches"] == []


def test_presenter_factory_selects_requested_format() -> None:
    assert isinstance(create_presenter(OutputFormat.TEXT), TextPresenter)
    assert isinstance(create_presenter(OutputFormat.JSON), JsonPresenter)
