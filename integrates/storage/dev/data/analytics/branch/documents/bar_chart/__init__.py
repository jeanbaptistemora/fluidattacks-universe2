from charts.utils import (
    CsvData,
)
from custom_exceptions import (
    UnsanitizedInputFound,
)
from decimal import (
    Decimal,
)
from newutils.validations import (
    validate_sanitized_csv_input,
)


def format_csv_data(
    *, document: dict, header: str = "Group name", alternative: str = ""
) -> CsvData:
    columns: list[list[str]] = document["data"]["columns"]
    values: list[Decimal] = document["originalValues"]
    categories: list[str] = document["axis"]["x"]["categories"]
    rows: list[list[str]] = []
    for category, value in zip(categories, values):
        try:
            validate_sanitized_csv_input(str(category).rsplit(" - ", 1)[0])
            rows.append([str(category).rsplit(" - ", 1)[0], str(value)])
        except UnsanitizedInputFound:
            rows.append(["", ""])

    return CsvData(
        headers=[header, alternative if alternative else columns[0][0]],
        rows=rows,
    )
