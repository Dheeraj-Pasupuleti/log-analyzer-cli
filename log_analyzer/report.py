import json
from datetime import datetime
from typing import Generator, Any


def format_report(
    entries: Generator[dict[str, object], None, None],
    fmt: str = "text",
) -> str:
    """Consume filtered entries and return text or JSON output."""
    results = list(entries)

    if not results:
        return "No log entries found matching the given filters."

    if fmt == "json":
        serializable: list[dict[str, Any]] = []

        for entry in results:
            timestamp = entry["timestamp"]
            if isinstance(timestamp, datetime):
                timestamp_value = timestamp.isoformat()
            else:
                timestamp_value = str(timestamp)

            serializable.append(
                {
                    **entry,
                    "timestamp": timestamp_value,
                }
            )

        return json.dumps(serializable, indent=2)

    lines: list[str] = []

    for entry in results:
        timestamp = entry["timestamp"]
        if isinstance(timestamp, datetime):
            timestamp_value = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp_value = str(timestamp)

        lines.append(
            f"[{entry['level']}] {timestamp_value} — {entry['message']}"
        )

    summary = f"\n--- {len(results)} entries found ---"
    return "\n".join(lines) + summary
