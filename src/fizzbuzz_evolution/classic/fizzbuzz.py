"""Classic textbook implementation of FizzBuzz."""


def fizzbuzz(number: int) -> str:
    """Return the classic FizzBuzz representation of a number."""
    if number % 15 == 0:
        return "FizzBuzz"
    if number % 3 == 0:
        return "Fizz"
    if number % 5 == 0:
        return "Buzz"
    return str(number)


def generate_fizzbuzz(start: int = 1, end: int = 100) -> list[str]:
    """Generate classic FizzBuzz values for an inclusive range."""
    return [fizzbuzz(number) for number in range(start, end + 1)]
