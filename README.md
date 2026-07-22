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
| `middle` | `03-middle` | Pure functions, separation of concerns, and stronger validation | Planned |
| `senior` | `04-senior` | Extensible rule engine | Planned |
| `enterprise` | `05-enterprise` | DDD, DI, configuration, CLI, and API | Planned |

Python package names cannot start with digits, so the numerical stage order is documented
while package directories use the names `classic`, `literal`, `middle`, `senior`, and
`enterprise`.

## Implemented behavior

Both implemented stages expose the same public functions:

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
│   └── 02-literal.md
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
