from charts.utils import (
    CsvData,
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
    return CsvData(
        headers=[header, *values],
        rows=[
            [
                category,
                *[str(counters[f"{category}/{value}"]) for value in values],
            ]
            for category in categories
        ],
    )
