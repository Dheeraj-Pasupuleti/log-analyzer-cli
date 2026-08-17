from datetime import datetime
from typing import Generator, Optional

from .exceptions import InvalidDateFormatError, InvalidLogLevelError

VALID_LEVELS = {"INFO", "WARN", "ERROR", "ALL"}


def filter_entries(
    entries: Generator[dict[str, object], None, None],
    level: str = "ALL",
    from_dt: Optional[datetime] = None,
    to_dt: Optional[datetime] = None,
) -> Generator[dict[str, object], None, None]:
    """Lazily filter entries by level and optional date range."""
    if level not in VALID_LEVELS:
        raise InvalidLogLevelError(f"Invalid level: {level}")

    if from_dt and to_dt and from_dt > to_dt:
        raise InvalidDateFormatError(
            "--from date must be before --to date"
        )

    for entry in entries:
        if level != "ALL" and entry["level"] != level:
            continue

        timestamp = entry["timestamp"]

        if from_dt and timestamp < from_dt:
            continue

        if to_dt and timestamp > to_dt:
            continue

        yield entry
