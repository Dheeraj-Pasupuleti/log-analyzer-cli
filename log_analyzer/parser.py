from datetime import datetime
from typing import Generator
import os

from .exceptions import LogAnalyzerError, MalformedLineError

LOG_LEVELS = {"INFO", "WARN", "ERROR"}


def read_log_file(
    path: str, max_errors: int = 10
) -> Generator[dict[str, object], None, None]:
    """Lazily read and parse log entries from a file."""
    if not os.path.isfile(path):
        raise LogAnalyzerError(f"File not found: {path}")

    error_count = 0

    with open(path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                yield parse_line(line)
            except MalformedLineError as exc:
                error_count += 1

                if error_count > max_errors:
                    raise MalformedLineError(
                        f"Too many malformed lines (>{max_errors}). "
                        "Aborting."
                    ) from exc

                print(
                    f"Warning: skipping malformed line {line_number}: {exc}"
                )


def parse_line(line: str) -> dict[str, object]:
    """Parse one line into timestamp, level and message."""
    parts = line.split(" ", 3)

    if len(parts) < 4:
        raise MalformedLineError(f"Cannot parse line: {line!r}")

    date_str, time_str, level, message = parts

    if level not in LOG_LEVELS:
        raise MalformedLineError(f"Unknown log level: {level!r}")

    try:
        timestamp = datetime.strptime(
            f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S"
        )
    except ValueError as exc:
        raise MalformedLineError(
            f"Invalid timestamp: {date_str} {time_str}"
        ) from exc

    return {
        "timestamp": timestamp,
        "level": level.strip(),
        "message": message.strip(),
    }
