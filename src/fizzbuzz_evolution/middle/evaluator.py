"""Evaluate individual values using the literal FizzBuzz rules."""


def evaluate(number: int) -> str:
    """Return the FizzBuzz representation of one integer."""
    result = ""

    if number % 3 == 0:
        result += "Fizz"

    if number % 5 == 0:
        result += "Buzz"

    return result or str(number)
