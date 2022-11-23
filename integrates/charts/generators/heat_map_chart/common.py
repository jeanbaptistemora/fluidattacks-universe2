from charts.utils import (
    CsvData,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    UnsanitizedInputFound,
)
from newutils.validations import (
    validate_sanitized_csv_input,
)
from typing import (
    Counter,
)


def format_csv_data(
    *,
    categories: list[str],
    values: list[str],
    counters: Counter[str],
    header: str,
) -> CsvData:
    headers_row: list[str] = [""]
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(header, *values)
        headers_row = [header, *values]

    rows: list[list[str]] = [[""]]
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(*categories)
        rows = [
            [
                category,
                *[str(counters[f"{category}/{value}"]) for value in values],
            ]
            for category in categories
        ]

    return CsvData(
        headers=headers_row,
        rows=rows,
    )
