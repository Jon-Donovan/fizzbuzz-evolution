# Implementation Comparison

FizzBuzz Evolution uses one stable behavior to compare different engineering approaches. The
stages are not a ranking from bad to good. Each stage is appropriate for a different problem
shape and expected rate of change.

| Aspect | Classic | Literal | Middle | Senior | Enterprise |
|---|---|---|---|---|---|
| Primary goal | Minimal textbook solution | Direct representation of independent rules | Separation and testability | Programmatic extensibility | Configurable application architecture |
| Evaluation model | Conditional branches | Independent conditions | Dedicated function | Ordered rule engine | Domain service and structured evaluations |
| Range generation | Local helper | Local helper | Separate generator | Engine-aware generator | Application use case |
| Validation | Minimal | Minimal | Explicit range error | Rule and range validation | Domain and configuration validation |
| Extension mechanism | Modify branches | Modify conditions | Modify evaluator | Register a rule | Configure rules through ports and YAML |
| Output | String | String | String | String | Structured result plus presenters |
| Infrastructure | None | None | CLI only | CLI only | YAML, logging, CLI, text and JSON presenters |
| Best fit | Teaching syntax | Discussing requirement interpretation | Small maintainable script | Reusable in-process rule library | Application boundary and integration example |

## Why Middle improves on Junior-style solutions

Middle separates evaluation, range generation, validation, and command-line interaction. The
algorithm remains simple, but each responsibility can be tested and changed independently.

## Why Senior differs from Middle

Middle decomposes a fixed algorithm. Senior makes the algorithm itself open to extension through
a rule contract and an immutable engine configuration.

## When Enterprise is justified

The Enterprise design becomes useful when configuration comes from outside the process, multiple
presentations are required, structured results must cross boundaries, or infrastructure concerns
need isolation from domain behavior.

## When Enterprise is excessive

For a one-off script or a stable two-rule exercise, ports, adapters, configuration models, and a
composition root add more concepts than the problem requires. The project includes that stage to
teach architectural boundaries, not to claim that every FizzBuzz implementation needs them.
