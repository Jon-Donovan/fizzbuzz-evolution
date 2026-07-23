"""Integration tests for YAML-to-presentation Enterprise pipelines."""

import json
from pathlib import Path

from fizzbuzz_evolution.enterprise import GenerateSequenceCommand
from fizzbuzz_evolution.enterprise.bootstrap import create_application_from_config
from fizzbuzz_evolution.enterprise.presentation.presenters import JsonPresenter, TextPresenter


def _write_extended_config(path: Path) -> None:
    path.write_text(
        """
version: 1
application:
  default_start: 105
  default_end: 105
  output_format: text
logging:
  level: WARNING
rules:
  - id: fizz
    type: divisibility
    divisor: 3
    replacement: Fizz
  - id: buzz
    type: divisibility
    divisor: 5
    replacement: Buzz
  - id: bazz
    type: divisibility
    divisor: 7
    replacement: Bazz
""",
        encoding="utf-8",
    )


def test_yaml_to_use_case_to_text(tmp_path: Path) -> None:
    path = tmp_path / "extended.yml"
    _write_extended_config(path)
    application = create_application_from_config(path)

    result = application.use_case.execute(GenerateSequenceCommand(105, 105))

    assert TextPresenter().present(result) == "FizzBuzzBazz"
    assert [match.rule_id.value for match in result.items[0].matches] == [
        "fizz",
        "buzz",
        "bazz",
    ]


def test_yaml_to_use_case_to_json(tmp_path: Path) -> None:
    path = tmp_path / "extended.yml"
    _write_extended_config(path)
    application = create_application_from_config(path)

    result = application.use_case.execute(GenerateSequenceCommand(7, 7))
    payload = json.loads(JsonPresenter().present(result))

    assert payload["items"][0]["value"] == "Bazz"
    assert payload["items"][0]["matches"][0]["rule_id"] == "bazz"
