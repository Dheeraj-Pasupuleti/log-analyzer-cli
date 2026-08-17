from datetime import datetime

import pytest

from log_analyzer.exceptions import InvalidDateFormatError
from log_analyzer.filters import filter_entries


def make_entries():
    yield {
        "timestamp": datetime(2024, 6, 10, 8, 0, 0),
        "level": "INFO",
        "message": "Hello",
    }
    yield {
        "timestamp": datetime(2024, 6, 10, 9, 0, 0),
        "level": "ERROR",
        "message": "Failed",
    }


def test_error_filter() -> None:
    result = list(filter_entries(make_entries(), "ERROR"))
    assert len(result) == 1
    assert result[0]["level"] == "ERROR"


def test_reversed_dates() -> None:
    with pytest.raises(InvalidDateFormatError):
        list(
            filter_entries(
                make_entries(),
                from_dt=datetime(2024, 6, 11),
                to_dt=datetime(2024, 6, 10),
            )
        )
