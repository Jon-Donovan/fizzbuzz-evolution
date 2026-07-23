# Installation

## Prerequisites

- Python 3.12 or newer
- Git

## Clone the repository

```bash
git clone https://github.com/Jon-Donovan/fizzbuzz-evolution.git
cd fizzbuzz-evolution
```

## Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install the project

Install the package in editable mode together with development dependencies:

```bash
pip install -e ".[test]"
```

> The editable installation only needs to be performed once. Reinstall the project only after changing package metadata or dependencies in `pyproject.toml`.

## Verify the installation

Run the quality checks:

```bash
ruff check .
mypy
pytest
```

## Run examples

```bash
python -m fizzbuzz_evolution.classic
python -m fizzbuzz_evolution.literal
python -m fizzbuzz_evolution.middle
python -m fizzbuzz_evolution.senior
python -m fizzbuzz_evolution.enterprise
```

Or use the Enterprise CLI:

```bash
fizzbuzz-enterprise --help
```
