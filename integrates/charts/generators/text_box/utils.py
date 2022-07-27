from charts.utils import (
    CsvData,
)
from typing_extensions import (
    TypedDict,
)

ForcesReport = TypedDict("ForcesReport", {"fontSizeRatio": float, "text": str})


def format_csv_data(*, header: str, value: str) -> CsvData:
    return CsvData(
        headers=[header],
        rows=[[value]],
    )
