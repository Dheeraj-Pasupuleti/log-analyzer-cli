# log-analyzer-cli

A beginner-friendly command-line tool to filter and analyze server log files.

## Features

- Generator-based, memory-efficient log reading
- INFO, WARN and ERROR level filtering
- Date range filtering
- Text and JSON reports
- Custom exception hierarchy
- `@timer` decorator using `functools.wraps`
- `argparse` CLI with help text and choices
- Defensive handling of common bad inputs
- Type hints throughout the package

## Project Structure

```text
log-analyzer-cli/
├── log_analyzer/
│   ├── __init__.py
│   ├── cli.py
│   ├── exceptions.py
│   ├── filters.py
│   ├── parser.py
│   └── report.py
├── tests/
│   ├── test_parser.py
│   └── test_filters.py
├── main.py
├── sample.log
├── requirements.txt
└── README.md
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Show all entries:

```bash
python main.py --file sample.log
```

Show only errors:

```bash
python main.py --file sample.log --level ERROR
```

Filter by date:

```bash
python main.py --file sample.log --from "2024-06-10 08:00:00" --to "2024-06-10 08:15:00"
```

Return JSON:

```bash
python main.py --file sample.log --level WARN --format json
```

Show help:

```bash
python main.py --help
```

## Log Format

Each valid line follows:

```text
TIMESTAMP LEVEL MESSAGE
```

Example:

```text
2024-06-10 14:32:01 ERROR Database connection timeout after 30s
```

## Code Review

Run:

```bash
flake8 log_analyzer/
mypy log_analyzer/
pytest
```

The project is designed around the dependency flow:

```text
Exceptions -> Parser -> Filters -> Report -> CLI
```
