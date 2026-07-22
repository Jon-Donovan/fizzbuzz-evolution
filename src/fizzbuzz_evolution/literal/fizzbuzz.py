"""Literal implementation of the independent FizzBuzz rules."""


def fizzbuzz(number: int) -> str:
    """Return the literal FizzBuzz representation of a number."""
    result = ""

    if number % 3 == 0:
        result += "Fizz"

    if number % 5 == 0:
        result += "Buzz"

    return result or str(number)


def generate_fizzbuzz(start: int = 1, end: int = 100) -> list[str]:
    """Generate literal FizzBuzz values for an inclusive range."""
    return [fizzbuzz(number) for number in range(start, end + 1)]
