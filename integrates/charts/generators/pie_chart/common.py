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


def format_csv_data(*, document: dict, header: list[str]) -> CsvData:
    columns: list[list[str]] = document["data"]["columns"]
    headers: list[str] = [""] * len(header)
    rows: list[list[str]] = []
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(*header)
        headers = [*header]

    for column in columns:
        try:
            validate_sanitized_csv_input(column[0], str(column[1]))
            rows.append([column[0], str(column[1])])
        except UnsanitizedInputFound:
            rows.append(["", ""])

    return CsvData(
        headers=headers,
        rows=rows,
    )
