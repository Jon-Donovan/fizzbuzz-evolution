"""Repository language policy tests."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEXT_TARGETS = (
    PROJECT_ROOT / "README.md",
    PROJECT_ROOT / "CHANGELOG.md",
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "src",
    PROJECT_ROOT / "tests",
    PROJECT_ROOT / "configs",
)
IGNORED_SUFFIXES = {".pyc"}


def _maintained_text_files() -> list[Path]:
    files: list[Path] = []
    for target in TEXT_TARGETS:
        candidates = (target,) if target.is_file() else target.rglob("*")
        files.extend(
            path for path in candidates if path.is_file() and path.suffix not in IGNORED_SUFFIXES
        )
    return files


def test_maintained_text_uses_english_only() -> None:
    violations: list[str] = []
    for path in _maintained_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if any("\u0400" <= character <= "\u04ff" for character in line):
                relative_path = path.relative_to(PROJECT_ROOT)
                violations.append(f"{relative_path}:{line_number}")

    assert not violations, "Cyrillic text found in maintained files: " + ", ".join(violations)
