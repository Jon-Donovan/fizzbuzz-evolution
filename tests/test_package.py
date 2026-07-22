"""Package metadata tests."""

from fizzbuzz_evolution import __version__


def test_package_version() -> None:
    assert __version__ == "0.4.1"
