# FizzBuzz Evolution

> One problem. Five stages of engineering evolution.

FizzBuzz Evolution is an educational Python project that demonstrates how one working
solution can evolve from a textbook exercise into a configurable application.

The central idea is simple:

> A junior developer can write a working solution. The deeper question is how closely the
> solution represents the domain and how safely it can evolve.

## Stages

| Package | Stage | Main idea | Status |
|---|---|---|---|
| `classic` | `01-classic` | Textbook solution with an explicit `% 15` branch | Implemented |
| `literal` | `02-literal` | Independent `Fizz` and `Buzz` conditions composed into a result | Implemented |
| `middle` | `03-middle` | Separate evaluator, generator, CLI, types, and validation | Implemented |
| `senior` | `04-senior` | Extensible rule engine | Implemented |
| `enterprise` | `05-enterprise` | Domain models, ports, use case, and structured results | Implemented |

Python package names cannot start with digits, so the numerical stage order is documented
while package directories use the names `classic`, `literal`, `middle`, `senior`, and
`enterprise`.

## Implemented behavior

The Classic and Literal stages expose the same public functions:

```python
fizzbuzz(number: int) -> str
generate_fizzbuzz(start: int = 1, end: int = 100) -> list[str]
```

They produce identical output but use different reasoning:

| Aspect | Classic | Literal |
|---|---|---|
| Combined case | Explicit `% 15` branch | Composition of independent matches |
| Control flow | Mutually exclusive branches | Independent conditions |
| Domain correspondence | Encodes a special combined case | Mirrors the stated rules |
| Extensibility | Low | Slightly better |
| Complexity | Minimal | Minimal |

Detailed explanations are available in:

- [01 — Classic](docs/01-classic.md)
- [02 — Literal](docs/02-literal.md)
- [03 — Middle](docs/03-middle.md)
- [04 — Senior](docs/04-senior.md)
- [05 — Enterprise Domain/Application](docs/05-enterprise-domain-application.md)

## Middle-stage API

The Middle stage separates responsibilities into focused modules:

```python
from fizzbuzz_evolution.middle import evaluate, generate

evaluate(15)       # "FizzBuzz"
generate(3, 5)     # ["Fizz", "4", "Buzz"]
```

A reversed range raises `InvalidRangeError` instead of silently returning an empty list.
Evaluation, range generation, and console interaction can be tested independently.

## Senior-stage API

The Senior stage replaces hard-coded conditions with an immutable, ordered rule engine:

```python
from fizzbuzz_evolution.senior import (
    CLASSIC_RULES,
    DivisibilityRule,
    RuleEngine,
    create_fizzbuzz_engine,
)

engine = create_fizzbuzz_engine()
engine.evaluate(15)  # "FizzBuzz"

extended = RuleEngine((*CLASSIC_RULES, DivisibilityRule(7, "Bazz")))
extended.evaluate(105)  # "FizzBuzzBazz"
```

Custom rules only need to implement the structural `Rule` protocol. The engine preserves
registration order and requires no modification when new rule types are introduced.

## Enterprise-stage API

The Enterprise stage introduces immutable domain models and an application use case:

```python
from fizzbuzz_evolution.enterprise import (
    GenerateSequenceCommand,
    create_fizzbuzz_use_case,
)

use_case = create_fizzbuzz_use_case()
result = use_case.execute(GenerateSequenceCommand(start=1, end=5))

[item.value for item in result.items]
# ["1", "2", "Fizz", "4", "Buzz"]

result.items[2].matches[0].rule_id.value
# "fizz"
```

The use case receives rules through the `RuleProvider` port and returns structured evaluations
that retain the source number and every matching rule output. CLI, external configuration, and
HTTP adapters remain intentionally outside this iteration.

## Requirements

- Python 3.12 or newer;
- pytest and pytest-cov as project test dependencies;
- Ruff and mypy as globally installed local development tools.

## Installation

```bash
python -m pip install -e ".[test]"
```

Ruff and mypy are intentionally not included in the project dependencies. They must be
available globally in the local development environment:

```bash
ruff --version
mypy --version
```

The CI workflow installs them explicitly because GitHub runners use isolated environments.

## Run

Classic implementation:

```bash
python -m fizzbuzz_evolution.classic
```

Literal implementation:

```bash
python -m fizzbuzz_evolution.literal
```

Both commands print the FizzBuzz sequence from 1 through 100.

Middle implementation:

```bash
python -m fizzbuzz_evolution.middle
python -m fizzbuzz_evolution.middle --start -5 --end 15
```

The Middle CLI supports custom inclusive bounds and reports reversed ranges as user-facing errors.

Senior implementation:

```bash
python -m fizzbuzz_evolution.senior
python -m fizzbuzz_evolution.senior --start -5 --end 15
```

The Senior CLI uses the classic preset while the public Python API supports custom rules.

## Quality checks

```bash
ruff check .
ruff format --check .
mypy
python -m pytest
```

## Project structure

```text
fizzbuzz-evolution/
├── docs/
│   ├── 01-classic.md
│   ├── 02-literal.md
│   ├── 03-middle.md
│   ├── 04-senior.md
│   └── 05-enterprise-domain-application.md
├── src/
│   └── fizzbuzz_evolution/
│       ├── classic/
│       ├── literal/
│       ├── middle/
│       ├── senior/
│       └── enterprise/
├── tests/
│   ├── classic/
│   ├── literal/
│   ├── middle/
│   ├── senior/
│   └── enterprise/
├── pyproject.toml
└── project.yml
```

## Language policy

Source code, comments, docstrings, command-line messages, and project documentation are
written in English. Translations, when needed, should be maintained separately.

## License

See [LICENSE](LICENSE).
