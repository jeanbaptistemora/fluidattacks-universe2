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
from typing_extensions import (
    TypedDict,
)

ForcesReport = TypedDict("ForcesReport", {"fontSizeRatio": float, "text": str})


def format_csv_data(*, header: str, value: str) -> CsvData:
    headers_row: list[str] = [""]
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(header)
        headers_row = [header]

    rows: list[list[str]] = [[""]]
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(value)
        rows = [[value]]

    return CsvData(headers=headers_row, rows=rows)
