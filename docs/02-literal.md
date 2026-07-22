# 02 — Literal

The literal stage follows the wording of the FizzBuzz rules directly.

## Algorithm

The implementation evaluates two independent conditions:

1. divisible by 3 → append `Fizz`;
2. divisible by 5 → append `Buzz`;
3. if nothing was appended → return the number itself.

A value such as `15` produces `FizzBuzz` through composition. There is no dedicated `% 15`
branch.

## Strengths

- each condition corresponds to one domain rule;
- combined output emerges naturally from matching multiple rules;
- adding another simple rule does not require enumerating combined divisors.

## Limitations

- divisors and replacement strings are still hard-coded;
- rules are not reusable objects;
- range generation and evaluation still live in the same small module.

## Run

```bash
python -m fizzbuzz_evolution.literal
```
