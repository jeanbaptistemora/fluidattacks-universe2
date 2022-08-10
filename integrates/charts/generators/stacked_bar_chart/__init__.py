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


def format_csv_data(*, document: dict, header: str) -> CsvData:
    columns: list[list[str]] = document["data"]["columns"]
    categories: list[str] = document["axis"]["x"]["categories"]
    headers: list[str] = [header] + [""] * len(columns)
    rows: list[list[str]] = []
    with suppress(UnsanitizedInputFound):
        values: list[str] = [column[0] for column in columns]
        validate_sanitized_csv_input(header, *values)
        headers = [header, *values]

    for index, category in enumerate(categories):
        temp_row: list[str] = [""]
        with suppress(UnsanitizedInputFound):
            temp_row[0] = category
        for column in columns:
            try:
                validate_sanitized_csv_input(str(column[index + 1]))
                temp_row.append(str(column[index + 1]))
            except UnsanitizedInputFound:
                temp_row.append("")
        rows.append(temp_row)

    return CsvData(
        headers=headers,
        rows=rows,
    )
