# 03 — Middle

The Middle stage keeps the literal FizzBuzz rules while separating evaluation, sequence
generation, error handling, and command-line interaction.

## Design

The package has four focused modules:

- `evaluator.py` transforms one integer into its FizzBuzz representation;
- `generator.py` validates and evaluates an inclusive range;
- `errors.py` defines expected application failures;
- `cli.py` parses user input, prints results, and maps failures to exit codes.

The module entry point delegates directly to `cli.main()` and contains no application logic.

## Public API

```python
from fizzbuzz_evolution.middle import evaluate, generate

evaluate(15)       # "FizzBuzz"
generate(3, 5)     # ["Fizz", "4", "Buzz"]
```

`evaluate()` is a pure function. It does not read input, print output, or depend on range
generation.

`generate()` returns values for an inclusive range. Equal bounds are valid, while a start
greater than the end raises `InvalidRangeError`.

## Boundary behavior

Zero and negative integers follow the same divisibility rules as positive integers:

```text
0   → FizzBuzz
-3  → Fizz
-5  → Buzz
-15 → FizzBuzz
```

A range may be negative or cross zero. A reversed range is rejected explicitly rather than
silently producing an empty list.

## CLI

Print the default range from 1 through 100:

```bash
python -m fizzbuzz_evolution.middle
```

Print a custom inclusive range:

```bash
python -m fizzbuzz_evolution.middle --start -5 --end 15
```

For an invalid range, the CLI writes a concise message to standard error and exits with code
`2` without displaying a traceback.

## Difference from the Junior stages

Classic and Literal demonstrate two small ways to express the algorithm. Middle demonstrates
how to make that algorithm safer to reuse and change:

| Concern | Classic / Literal | Middle |
|---|---|---|
| One-number evaluation | Shares a module with range generation | Dedicated evaluator |
| Range generation | No invalid-range contract | Inclusive range with validation |
| Console interaction | Direct module entry point | Testable CLI function |
| Expected failures | Implicit behavior | Typed exception hierarchy |
| Tests | Algorithm and basic range | Components, boundaries, errors, and CLI |

The stage deliberately avoids configurable rule objects and dependency injection. Those
belong to the Senior and Enterprise stages.
