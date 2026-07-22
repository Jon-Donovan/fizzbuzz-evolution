# 05 — Enterprise Domain/Application

The Enterprise stage introduces explicit domain and application boundaries around the same
FizzBuzz behavior implemented by the previous stages. It deliberately stops before adding
configuration files, persistence, HTTP delivery, logging, metrics, or a dependency injection
container.

## Goal

The Senior stage makes the algorithm extensible through ordered rules. The Enterprise stage
makes the system boundaries and business data explicit:

- domain values are represented by immutable models;
- rule matches retain stable identifiers;
- evaluation returns structured data instead of a plain string;
- range generation is expressed as an application use case;
- rule acquisition is hidden behind an application port.

## Package structure

```text
enterprise/
├── application/
│   ├── commands.py
│   ├── ports.py
│   ├── results.py
│   └── use_cases.py
├── domain/
│   ├── errors.py
│   ├── models.py
│   ├── rules.py
│   └── services.py
├── bootstrap.py
└── presets.py
```

Dependencies point inward. The application layer uses domain models and services, while the
domain layer has no dependency on application code, CLI frameworks, storage, or serialization.

## Domain models

`Number` represents an evaluated integer. `RuleId` gives each rule a stable identity.
`RuleOutput` records one matching rule result, and `Evaluation` records the complete result for
one number.

```python
Evaluation(
    number=Number(15),
    value="FizzBuzz",
    matches=(
        RuleOutput(rule_id=RuleId("fizz"), value="Fizz"),
        RuleOutput(rule_id=RuleId("buzz"), value="Buzz"),
    ),
)
```

Unlike a plain string, this result can later be serialized, logged, measured, or rendered by
multiple delivery adapters without re-running the rules.

`NumberRange` owns the inclusive-range invariant. A reversed range raises `InvalidRangeError`
when the model is created.

## Rule contract

Enterprise rules implement a structural protocol:

```python
class Rule(Protocol):
    @property
    def rule_id(self) -> RuleId: ...

    def matches(self, number: Number) -> bool: ...

    def apply(self, number: Number) -> RuleOutput: ...
```

`DivisibilityRule` is the built-in implementation. It rejects a zero divisor and empty
replacement text while preserving support for zero, negative numbers, and negative divisors.

## Evaluation service

`EvaluationService` materializes an ordered rule iterable and evaluates one `Number`. All
matching outputs are retained in registration order. When no rule matches, the original number
is rendered as text.

The service has no knowledge of classic FizzBuzz constants. Those values belong to the
`CLASSIC_RULES` preset.

## Application port

`RuleProvider` is the input boundary used by the application layer:

```python
class RuleProvider(Protocol):
    def get_rules(self) -> tuple[Rule, ...]: ...
```

The use case does not know whether rules came from an in-memory preset, JSON, YAML, a database,
or a remote service. Future infrastructure adapters can implement this port without changing
the use case.

## Use case

`GenerateSequenceUseCase` accepts a `GenerateSequenceCommand` and returns a
`GenerateSequenceResult`:

```python
use_case = create_fizzbuzz_use_case()
result = use_case.execute(GenerateSequenceCommand(start=1, end=5))

[item.value for item in result.items]
# ["1", "2", "Fizz", "4", "Buzz"]
```

The use case performs application orchestration only:

1. create and validate a domain range;
2. request rules through the port;
3. create the domain evaluation service;
4. evaluate every number;
5. return an immutable structured result.

It does not print output, parse arguments, load files, serialize JSON, or depend on a web
framework.

## Composition

`StaticRuleProvider` is a minimal local adapter used by the composition helper. The
`create_fizzbuzz_use_case()` function creates a ready-to-use application with the classic rule
preset.

This is manual dependency injection: dependencies are supplied explicitly through constructors
without introducing a container.

## Testing strategy

Domain tests cover:

- range invariants and inclusive iteration;
- rule identifier validation;
- divisibility rule invariants;
- immutable models;
- ordered structured evaluation;
- custom structural rules;
- materialization of rule iterables.

Application tests use a stub `RuleProvider` and verify:

- structured sequence results;
- negative and zero values;
- empty rule sets;
- one provider call per execution;
- validation before dependency access.

The shared stage contract adapts the Enterprise structured result back to a string and confirms
that all five stages still produce the same observable FizzBuzz values.

## Intentional boundary

This iteration does not include:

- CLI or HTTP adapters;
- JSON or YAML configuration;
- repositories or persistence;
- dependency injection containers;
- logging, metrics, or tracing;
- serialization DTOs;
- integration tests;
- Docker or deployment configuration.

Those concerns belong to later Enterprise infrastructure and delivery iterations. Keeping them
out of this stage makes the domain/application transition visible and independently testable.
