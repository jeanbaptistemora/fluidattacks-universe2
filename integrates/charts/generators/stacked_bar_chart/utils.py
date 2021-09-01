from charts.colors import (
    RISK,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from typing import (
    cast,
    Dict,
    List,
    NamedTuple,
    Tuple,
    Union,
)

# Constants
DATE_FMT: str = "%Y - %m - %d"
# Let's no over think it
MONTH_TO_NUMBER = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

# Typing
GroupDocumentData = NamedTuple(
    "GroupDocumentData",
    [
        ("accepted", float),
        ("closed", float),
        ("opened", float),
        ("date", datetime),
        ("total", float),
    ],
)


def translate_date(date_str: str) -> datetime:
    # No, there is no smarter way because of locales and that weird format

    parts = date_str.replace(",", "").replace("- ", "").split(" ")

    if len(parts) == 6:
        date_year, date_month, date_day = parts[2], parts[0], parts[1]
    elif len(parts) == 5:
        date_year, date_month, date_day = parts[4], parts[0], parts[1]
    elif len(parts) == 4:
        date_year, date_month, date_day = parts[3], parts[0], parts[1]
    else:
        raise ValueError(f"Unexpected number of parts: {parts}")

    return datetime(int(date_year), MONTH_TO_NUMBER[date_month], int(date_day))


def format_document(
    document: Dict[str, Dict[datetime, float]],
    y_label: str,
    tick_format: bool = True,
) -> dict:
    return dict(
        data=dict(
            x="date",
            columns=[
                cast(List[Union[Decimal, str]], [name])
                + [
                    date.strftime(DATE_FMT)
                    if name == "date"
                    else Decimal(document[name][date]).quantize(Decimal("0.1"))
                    for date in tuple(document["date"])[-12:]
                ]
                for name in document
            ],
            colors={
                "Closed": RISK.more_passive,
                "Accepted": RISK.agressive,
                "Found": RISK.more_agressive,
            },
            types={
                "Closed": "line",
                "Accepted": "line",
                "Found": "line",
            },
        ),
        axis=dict(
            x=dict(
                tick=dict(
                    centered=True,
                    multiline=False,
                    rotate=12,
                ),
                type="category",
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
                label=dict(
                    text=y_label,
                    position="inner-top",
                ),
            ),
        ),
        grid=dict(
            x=dict(
                show=True,
            ),
            y=dict(
                show=True,
            ),
        ),
        legend=dict(
            position="bottom",
        ),
        point=dict(
            focus=dict(
                expand=dict(
                    enabled=True,
                ),
            ),
            r=5,
        ),
        barChartYTickFormat=tick_format,
    )


def format_distribution_document(
    document: Dict[str, Dict[datetime, float]],
    y_label: str,
    tick_format: bool = True,
) -> dict:
    return dict(
        data=dict(
            x="date",
            columns=[
                cast(List[Union[Decimal, str]], [name])
                + [
                    date.strftime(DATE_FMT)
                    if name == "date"
                    else Decimal(document[name][date]).quantize(Decimal("0.1"))
                    for date in tuple(document["date"])[-12:]
                ]
                for name in document
            ],
            colors={
                "Closed": RISK.more_passive,
                "Accepted": RISK.agressive,
                "Open": RISK.more_agressive,
            },
            groups=[
                [
                    "Closed",
                    "Accepted",
                    "Open",
                ]
            ],
            type="bar",
            order=None,
            stack=dict(
                normalize=True,
            ),
        ),
        axis=dict(
            x=dict(
                tick=dict(
                    centered=True,
                    multiline=False,
                    rotate=12,
                ),
                type="category",
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
                label=dict(
                    text=y_label,
                    position="inner-top",
                ),
            ),
        ),
        grid=dict(
            x=dict(
                show=True,
            ),
            y=dict(
                show=True,
            ),
        ),
        legend=dict(
            position="bottom",
        ),
        point=dict(
            focus=dict(
                expand=dict(
                    enabled=True,
                ),
            ),
            r=5,
        ),
        barChartYTickFormat=tick_format,
    )


def sum_over_time_many_groups(
    group_documents: Tuple[Dict[str, Dict[datetime, float]], ...],
    documents_names: List[str],
) -> Dict[str, Dict[datetime, float]]:
    all_dates: List[datetime] = sorted(
        set(
            date
            for group_document in group_documents
            for date in group_document["date"]
        )
    )

    for group_document in group_documents:
        for name in group_document:
            last_date = None
            for date in all_dates:
                if date in group_document[name]:
                    last_date = date
                elif last_date:
                    group_document[name][date] = group_document[name][
                        last_date
                    ]
                else:
                    group_document[name][date] = 0

    return {
        name: {
            date: sum(
                group_document[name].get(date, 0)
                for group_document in group_documents
            )
            for date in all_dates
        }
        for name in documents_names
    }
