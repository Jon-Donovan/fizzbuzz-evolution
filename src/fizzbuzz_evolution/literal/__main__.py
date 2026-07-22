"""Run the literal FizzBuzz implementation."""

from .fizzbuzz import generate_fizzbuzz


def main() -> None:
    """Print literal FizzBuzz values from 1 through 100."""
    print(*generate_fizzbuzz(), sep="\n")


if __name__ == "__main__":
    main()
