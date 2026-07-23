# 06 — Enterprise Infrastructure and Presentation

Iteration 6 turns the Enterprise domain/application core into a runnable, configurable
application. The dependency direction remains explicit:

```text
Presentation -> Application -> Domain
Infrastructure --------------^ 
```

The domain does not import YAML, `argparse`, JSON, paths, or logging configuration. The
application use case still depends only on the `RuleProvider` port.

## Configuration

The Enterprise CLI can load a versioned YAML file:

```yaml
version: 1

application:
  default_start: 1
  default_end: 100
  output_format: text

logging:
  level: WARNING

rules:
  - id: fizz
    type: divisibility
    divisor: 3
    replacement: Fizz
  - id: buzz
    type: divisibility
    divisor: 5
    replacement: Buzz
```

The loader validates the external shape before constructing typed configuration models. Domain
objects perform the final validation of domain invariants such as non-zero divisors, meaningful
rule identifiers, and non-empty replacements.

Supported configuration values:

- configuration version: `1`;
- output formats: `text`, `json`;
- log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`;
- rule type: `divisibility`.

Rules preserve their YAML registration order. Therefore a configuration that declares `buzz`
before `fizz` produces `BuzzFizz` for `15`.

## Precedence

Effective settings use the following precedence:

```text
CLI arguments > YAML configuration > built-in defaults
```

A YAML file can define `default_end: 100`, while `--end 30` limits the actual request to `30`.

## CLI

Run the module directly:

```bash
python -m fizzbuzz_evolution.enterprise
python -m fizzbuzz_evolution.enterprise --start 14 --end 16
python -m fizzbuzz_evolution.enterprise --config configs/fizzbuzz.yml
python -m fizzbuzz_evolution.enterprise --format json
```

An installed console script is also available:

```bash
fizzbuzz-enterprise --config configs/fizzbuzz.yml
```

Supported options:

```text
--start INTEGER
--end INTEGER
--config PATH
--format {text,json}
--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
```

## Presenters

`TextPresenter` renders one value per line and does not add a trailing newline. The CLI owns the
output side effect and uses `print()`.

`JsonPresenter` explicitly maps application results to a stable public structure:

```json
{
  "start": 3,
  "end": 3,
  "items": [
    {
      "number": 3,
      "value": "Fizz",
      "matches": [
        {
          "rule_id": "fizz",
          "value": "Fizz"
        }
      ]
    }
  ]
}
```

The presenter does not serialize dataclasses implicitly. This prevents internal model changes
from accidentally changing the public JSON contract.

## Output and logging

The process keeps result and diagnostic channels separate:

```text
stdout -> text or JSON sequence result
stderr -> logs and user-facing errors
```

This makes redirection safe:

```bash
fizzbuzz-enterprise --format json > result.json
```

The standard logging module is configured centrally. `INFO` records application start and
completion, while `DEBUG` includes configured rule identifiers. The application does not log one
record per evaluated number.

## Exit codes

The CLI exposes stable exit codes:

| Code | Meaning |
|---:|---|
| `0` | Success |
| `1` | Unexpected internal failure |
| `2` | Invalid command-line arguments |
| `3` | Configuration failure |
| `4` | Domain validation failure |

Expected user errors are printed without a traceback.

## Testing strategy

Unit tests cover configuration parsing, validation, the configured rule provider, presenters,
and CLI behavior.

Integration tests connect real YAML files to the composition root, use case, and presenters.
They verify the complete in-process path:

```text
YAML -> typed config -> domain rules -> use case -> presenter
```

Acceptance tests execute the module in a subprocess and verify stdout, stderr, JSON validity, and
process exit codes.

## Scope boundary

This iteration intentionally does not add HTTP, OpenAPI, databases, dependency injection
frameworks, metrics, distributed tracing, Docker, or dynamic Python imports from configuration.
The completed vertical slice is:

```text
YAML -> configuration -> RuleProvider -> use case
     -> structured result -> text/JSON -> CLI
```
