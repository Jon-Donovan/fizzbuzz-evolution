# 01 — Classic

The classic stage presents the textbook FizzBuzz solution.

## Algorithm

The implementation checks divisibility in this order:

1. divisible by 15 → `FizzBuzz`;
2. divisible by 3 → `Fizz`;
3. divisible by 5 → `Buzz`;
4. otherwise → the number itself.

The combined case must be checked first. Otherwise, a number such as `15` would match the
`3` branch before the program could return `FizzBuzz`.

## Strengths

- minimal and easy to recognize;
- straightforward control flow;
- suitable for explaining condition ordering.

## Limitations

- the combined `% 15` branch duplicates knowledge already implied by the `% 3` and `% 5`
  rules;
- adding another word requires adding more combined cases;
- the implementation is tied directly to the classic FizzBuzz rules.

## Run

```bash
python -m fizzbuzz_evolution.classic
```
