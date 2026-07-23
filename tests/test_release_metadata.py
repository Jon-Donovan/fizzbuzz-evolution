"""Release metadata consistency tests."""

import tomllib
from pathlib import Path

import yaml

from fizzbuzz_evolution import __version__

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_version_is_consistent_across_release_metadata() -> None:
    pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project_config = yaml.safe_load((PROJECT_ROOT / "project.yml").read_text(encoding="utf-8"))

    assert pyproject["project"]["version"] == __version__
    assert project_config["version"]["ver"] == __version__
    assert project_config["version"]["build"].startswith(f"{__version__}.")


def test_release_documentation_exists() -> None:
    expected_documents = (
        PROJECT_ROOT / "docs" / "07-completion.md",
        PROJECT_ROOT / "docs" / "comparison.md",
        PROJECT_ROOT / "docs" / "adr" / "0001-iterative-evolution.md",
        PROJECT_ROOT / "docs" / "adr" / "0002-rule-engine.md",
        PROJECT_ROOT / "docs" / "adr" / "0003-ports-and-adapters.md",
        PROJECT_ROOT / "docs" / "adr" / "0004-yaml-configuration.md",
        PROJECT_ROOT / "docs" / "adr" / "0005-english-language-policy.md",
    )

    assert all(path.is_file() for path in expected_documents)
