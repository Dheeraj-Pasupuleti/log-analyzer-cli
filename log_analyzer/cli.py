import argparse
import functools
import os
import sys
import time
from datetime import datetime
from typing import Any, Callable

from .exceptions import InvalidDateFormatError, LogAnalyzerError
from .filters import filter_entries
from .parser import read_log_file
from .report import format_report


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Print how long the wrapped function takes to execute."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(
            f"[timer] {func.__name__} completed in {elapsed:.4f}s"
        )
        return result

    return wrapper


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze log files by level and date range."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the log file (e.g. server.log)",
    )
    parser.add_argument(
        "--level",
        default="ALL",
        choices=["ALL", "INFO", "WARN", "ERROR"],
        help="Filter by log level (default: ALL)",
    )
    parser.add_argument(
        "--from",
        dest="from_dt",
        default=None,
        help="Start datetime: YYYY-MM-DD HH:MM:SS",
    )
    parser.add_argument(
        "--to",
        dest="to_dt",
        default=None,
        help="End datetime: YYYY-MM-DD HH:MM:SS",
    )
    parser.add_argument(
        "--format",
        dest="fmt",
        default="text",
        choices=["text", "json"],
        help="Output format: text or json (default: text)",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    """Validate paths and convert date strings into datetime objects."""
    if os.path.isdir(args.file):
        raise LogAnalyzerError(
            f"{args.file!r} is a directory, not a file."
        )

    date_format = "%Y-%m-%d %H:%M:%S"

    if args.from_dt:
        original_from = args.from_dt
        try:
            args.from_dt = datetime.strptime(args.from_dt, date_format)
        except ValueError as exc:
            raise InvalidDateFormatError(
                f"Invalid --from date: {original_from!r}"
            ) from exc

    if args.to_dt:
        original_to = args.to_dt
        try:
            args.to_dt = datetime.strptime(args.to_dt, date_format)
        except ValueError as exc:
            raise InvalidDateFormatError(
                f"Invalid --to date: {original_to!r}"
            ) from exc


@timer
def run_analysis(args: argparse.Namespace) -> None:
    """Run the complete parser -> filter -> report pipeline."""
    validate_args(args)

    entries = read_log_file(args.file)
    filtered = filter_entries(
        entries,
        level=args.level,
        from_dt=args.from_dt,
        to_dt=args.to_dt,
    )
    report = format_report(filtered, args.fmt)
    print(report)


def main() -> None:
    args = parse_args()

    try:
        run_analysis(args)
    except LogAnalyzerError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
