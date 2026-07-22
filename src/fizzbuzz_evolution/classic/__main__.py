"""Run the classic FizzBuzz implementation."""

from .fizzbuzz import generate_fizzbuzz


def main() -> None:
    """Print classic FizzBuzz values from 1 through 100."""
    print(*generate_fizzbuzz(), sep="\n")


if __name__ == "__main__":
    main()
