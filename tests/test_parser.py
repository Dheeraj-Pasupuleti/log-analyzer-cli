from datetime import datetime

import pytest

from log_analyzer.exceptions import MalformedLineError
from log_analyzer.parser import parse_line, read_log_file


def test_parse_line() -> None:
    result = parse_line(
        "2024-06-10 08:00:01 INFO Server started"
    )
    assert result["level"] == "INFO"
    assert result["message"] == "Server started"
    assert result["timestamp"] == datetime(2024, 6, 10, 8, 0, 1)


def test_parse_malformed_line() -> None:
    with pytest.raises(MalformedLineError):
        parse_line("not a valid log line")


def test_generator_reads_entries(tmp_path) -> None:
    path = tmp_path / "test.log"
    path.write_text(
        "2024-06-10 08:00:01 INFO Hello\n"
        "2024-06-10 08:01:01 ERROR Failed\n",
        encoding="utf-8",
    )

    entries = read_log_file(str(path))
    assert not isinstance(entries, list)
    assert len(list(entries)) == 2
