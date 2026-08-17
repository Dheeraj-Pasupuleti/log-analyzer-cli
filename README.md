# Log Analyzer CLI

A Python command-line application for analyzing log files by log level and date/time range.

The application reads a log file, validates each entry, skips malformed records with warnings, filters valid entries based on user-specified criteria, and displays the results in text or JSON format.

## Features

- Parse and validate log files
- Skip malformed log entries with warnings
- Filter by `INFO`, `WARN`, `ERROR`, or `ALL`
- Filter by date/time range
- Text or JSON output
- Command-line interface using `argparse`
- Execution-time measurement
- Automatic virtual-environment setup with `run.sh`
- Dependencies installed only on the first run
- Testing with `pytest`
- Linting with `flake8`
- Static type checking with `mypy`

## Project Structure

```text
log-analyzer-cli/
├── main.py
├── run.sh
├── sample.log
├── empty.log
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── log_analyzer/
│   ├── __init__.py
│   ├── cli.py
│   ├── parser.py
│   ├── filters.py
│   ├── report.py
│   └── exceptions.py
└── tests/
    ├── test_filters.py
    └── test_parser.py
```

## Requirements

- Python 3
- macOS/Linux shell environment

The project creates a local `.venv` virtual environment automatically when you run `run.sh` for the first time.

## Quick Start

Clone the repository:

```bash
git clone <repository-url>
cd log-analyzer-cli
```

Make the script executable:

```bash
chmod +x run.sh
```

Run the application:

```bash
./run.sh --file sample.log
```

### First Run

On the first run, `run.sh`:

1. Checks that Python 3 is installed.
2. Creates `.venv` if it does not exist.
3. Installs dependencies from `requirements.txt`.
4. Runs the Log Analyzer.

### Subsequent Runs

If `.venv` already exists, the script skips virtual-environment creation and dependency installation.

```bash
./run.sh --file sample.log
```

If `requirements.txt` is changed later, update the existing environment manually:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

## Usage

### Analyze all valid entries

```bash
./run.sh --file sample.log
```

The default log level is `ALL`.

### Filter by log level

```bash
./run.sh --file sample.log --level INFO
```

```bash
./run.sh --file sample.log --level WARN
```

```bash
./run.sh --file sample.log --level ERROR
```

```bash
./run.sh --file sample.log --level ALL
```

### Filter by start date/time

```bash
./run.sh --file sample.log --from "2024-06-10 08:00:00"
```

### Filter by end date/time

```bash
./run.sh --file sample.log --to "2024-06-10 08:20:00"
```

### Filter by a date/time range

```bash
./run.sh \
  --file sample.log \
  --from "2024-06-10 08:00:00" \
  --to "2024-06-10 08:20:00"
```

### Combine level and date filters

```bash
./run.sh \
  --file sample.log \
  --level ERROR \
  --from "2024-06-10 08:00:00" \
  --to "2024-06-11 10:00:00"
```

### JSON output

```bash
./run.sh \
  --file sample.log \
  --level ERROR \
  --format json
```

Example:

```json
[
  {
    "timestamp": "2024-06-10T08:15:44",
    "level": "ERROR",
    "message": "Database connection failed: timeout"
  },
  {
    "timestamp": "2024-06-10T08:20:55",
    "level": "ERROR",
    "message": "Retry attempt 1 of 3"
  },
  {
    "timestamp": "2024-06-11T09:05:00",
    "level": "ERROR",
    "message": "Backup failed: permission denied"
  }
]
```

### Display help

```bash
./run.sh --help
```

## Command-Line Options

| Option | Description | Default |
|---|---|---|
| `--file FILE` | Path to the log file | Required |
| `--level {ALL,INFO,WARN,ERROR}` | Filter by log level | `ALL` |
| `--from FROM_DT` | Start datetime (`YYYY-MM-DD HH:MM:SS`) | None |
| `--to TO_DT` | End datetime (`YYYY-MM-DD HH:MM:SS`) | None |
| `--format {text,json}` | Output format | `text` |

## Example Log File

```text
[INFO] 2024-06-10 08:00:01 — Server started on port 8080
[INFO] 2024-06-10 08:05:12 — Request received: GET /api/health
[WARN] 2024-06-10 08:10:33 — Memory usage at 82%
[ERROR] 2024-06-10 08:15:44 — Database connection failed: timeout
[ERROR] 2024-06-10 08:20:55 — Retry attempt 1 of 3
[INFO] 2024-06-10 08:25:01 — Retry succeeded
[WARN] 2024-06-10 08:30:22 — Disk usage at 91%
[INFO] 2024-06-11 09:00:00 — Daily backup started
[ERROR] 2024-06-11 09:05:00 — Backup failed: permission denied
[INFO] 2024-06-11 09:10:00 — Backup completed
```

The sample also demonstrates malformed records. For example:

```text
Warning: skipping malformed line 7: Unknown log level: 'IS'
Warning: skipping malformed line 12: Invalid timestamp: BAD TIMESTAMP
```

Malformed entries are skipped rather than stopping the entire analysis.

## Example Output

Running:

```bash
./run.sh --file sample.log
```

produces the valid log entries followed by:

```text
--- 10 entries found ---
```

For the sample used with this project, two malformed lines are skipped, leaving 10 valid entries.

## Architecture

```text
main.py
   │
   ▼
cli.py
   │
   ├── parser.py
   │      └── Reads and validates log entries
   │
   ├── filters.py
   │      └── Applies level and date filters
   │
   ├── report.py
   │      └── Formats text/JSON output
   │
   └── exceptions.py
          └── Custom application errors
```

### Modules

- **`main.py`** — application entry point.
- **`cli.py`** — parses command-line arguments and coordinates the workflow.
- **`parser.py`** — reads and validates log entries.
- **`filters.py`** — applies log-level and date/time filters.
- **`report.py`** — produces text and JSON output.
- **`exceptions.py`** — custom application exceptions.

## Testing

The project uses `pytest`.

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the complete test suite:

```bash
python -m pytest
```

Current test suite:

```text
5 passed
```

The tests cover log parsing and filtering behavior.

Run individual test files:

```bash
python -m pytest tests/test_parser.py
```

```bash
python -m pytest tests/test_filters.py
```

Using `python -m pytest` ensures pytest runs with the currently active Python interpreter and project environment.

## Code Quality

Run `flake8`:

```bash
.venv/bin/flake8 log_analyzer/
```

A clean Flake8 run produces no output and returns exit code `0`.

Run `mypy`:

```bash
.venv/bin/mypy log_analyzer/
```

The project requirements currently include `flake8`, `mypy`, and `pytest`.

## `run.sh`

`run.sh` provides a single executable entry point:

```bash
./run.sh --file sample.log
```

Its setup logic is intentionally performed only when `.venv` does not exist.

The workflow is:

```text
First run:
run.sh
  ↓
check Python
  ↓
create .venv
  ↓
install requirements
  ↓
run application

Later runs:
run.sh
  ↓
use existing .venv
  ↓
run application
```

This prevents dependency installation from happening every time the application is executed.

The virtual environment should not be committed to GitHub. Add the following to `.gitignore`:

```text
.venv/
__pycache__/
*.pyc
.pytest_cache/
```

## Error Handling

The application handles:

- Unknown log levels
- Invalid timestamps
- Malformed log entries
- Missing input files
- Invalid command-line arguments

Malformed log entries are skipped and reported as warnings.

## License

This project is open source and is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for the complete license text.

The MIT License permits use, modification, distribution, and commercial use, subject to its conditions.
