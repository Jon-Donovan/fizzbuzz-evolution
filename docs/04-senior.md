# Iteration 4 — Senior

## Goal

The Senior stage replaces hard-coded FizzBuzz conditions with an extensible, ordered rule
engine. New behavior is introduced by registering another rule rather than modifying the
engine.

## Design

The stage contains four responsibilities:

- `Rule` defines the structural contract required by the engine;
- `DivisibilityRule` implements reusable divisibility-based replacement;
- `RuleEngine` evaluates one number against an immutable ordered rule collection;
- `generate` and the CLI handle sequence generation and presentation.

The rule contract uses `Protocol`, so custom rules do not need to inherit from a framework base
class. The engine only depends on behavior: a rule must decide whether it matches and render its
result.

## Ordering

Every matching rule contributes text in registration order. The engine does not sort by divisor,
name, or priority. This keeps composition explicit and predictable.

```python
from fizzbuzz_evolution.senior import DivisibilityRule, RuleEngine

engine = RuleEngine(
    (
        DivisibilityRule(3, "Fizz"),
        DivisibilityRule(5, "Buzz"),
        DivisibilityRule(7, "Bazz"),
    )
)

assert engine.evaluate(105) == "FizzBuzzBazz"
```

## Validation

`DivisibilityRule` rejects a zero divisor and blank replacement text. Rule collections are
materialized as tuples so later changes to an input list cannot mutate a configured engine.
Reversed ranges raise the stage-specific `InvalidRangeError`.

## Extension example

A custom rule can satisfy the protocol without inheriting from `DivisibilityRule`:

```python
class NegativeRule:
    def matches(self, number: int) -> bool:
        return number < 0

    def render(self, number: int) -> str:
        return f"Negative({number})"
```

Registering this object extends the engine without changing engine source code. This demonstrates
the Open/Closed Principle at a scale appropriate for the exercise.

## Boundary with Enterprise

The Senior stage supports programmatic configuration in Python. It deliberately does not include
YAML loading, application ports, structured domain results, logging configuration, or
infrastructure adapters. Those concerns belong to the Enterprise stages.
