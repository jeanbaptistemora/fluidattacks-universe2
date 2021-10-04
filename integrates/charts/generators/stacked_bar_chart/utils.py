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
    Any,
    Dict,
    List,
    NamedTuple,
    Tuple,
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

DISTRIBUTION_OVER_TIME: List[str] = [
    "date",
    "Closed",
    "Accepted",
    "Open",
]

RISK_OVER_TIME: List[str] = [
    "date",
    "Closed",
    "Accepted",
    "Found",
]

EXPOSED_OVER_TIME: List[str] = [
    "date",
    "Exposure",
]

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


class RiskOverTime(NamedTuple):
    # pylint: disable=inherit-non-class, too-few-public-methods
    monthly: Dict[str, Dict[datetime, float]]
    weekly: Dict[str, Dict[datetime, float]]
    should_use_monthly: bool


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


def translate_date_last(date_str: str) -> datetime:
    parts = date_str.replace(",", "").replace("- ", "").split(" ")

    if len(parts) == 6:
        date_year, date_month, date_day = parts[5], parts[3], parts[4]
    elif len(parts) == 5:
        date_year, date_month, date_day = parts[4], parts[2], parts[3]
    elif len(parts) == 4:
        date_year, date_month, date_day = parts[3], parts[0], parts[2]
    else:
        raise ValueError(f"Unexpected number of parts: {parts}")

    return datetime(int(date_year), MONTH_TO_NUMBER[date_month], int(date_day))


def format_document(
    document: Dict[str, Dict[datetime, float]],
    y_label: str,
    tick_format: bool = True,
) -> Dict[str, Any]:
    return dict(
        data=dict(
            x="date",
            columns=[
                [name]
                + [
                    date.strftime(DATE_FMT)
                    if name == "date"
                    else str(
                        Decimal(document[name][date]).quantize(Decimal("0.1"))
                    )
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
) -> Dict[str, Any]:
    return dict(
        data=dict(
            x="date",
            columns=[
                [name]
                + [
                    date.strftime(DATE_FMT)
                    if name == "date"
                    else str(
                        Decimal(document[name][date]).quantize(Decimal("0.1"))
                    )
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
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
        normalizedToolTip=True,
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


def get_data_risk_over_time_group(
    *,
    over_time_weekly: List[List[Dict[str, float]]],
    over_time_monthly: List[List[Dict[str, float]]],
    weekly_data_size: int,
    limited_days: bool,
) -> RiskOverTime:
    data: List[GroupDocumentData] = []
    data_monthly: List[GroupDocumentData] = []
    if over_time_weekly:
        group_found_over_time = over_time_weekly[0]
        group_closed_over_time = over_time_weekly[1]
        group_accepted_over_time = over_time_weekly[2]

        for accepted, closed, found in zip(
            group_accepted_over_time,
            group_closed_over_time,
            group_found_over_time,
        ):
            data.append(
                GroupDocumentData(
                    accepted=accepted["y"],
                    closed=closed["y"],
                    opened=found["y"] - closed["y"] - accepted["y"],
                    date=translate_date(str(found["x"])),
                    total=found["y"],
                )
            )

    if over_time_monthly:
        group_found_over_time = over_time_monthly[0]
        group_closed_over_time = over_time_monthly[1]
        group_accepted_over_time = over_time_monthly[2]

        for accepted, closed, found in zip(
            group_accepted_over_time,
            group_closed_over_time,
            group_found_over_time,
        ):
            data_monthly.append(
                GroupDocumentData(
                    accepted=accepted["y"],
                    closed=closed["y"],
                    opened=found["y"] - closed["y"] - accepted["y"],
                    date=(
                        translate_date_last(str(found["x"]))
                        if translate_date_last(str(found["x"]))
                        < datetime.now()
                        else datetime.combine(
                            datetime.now(),
                            datetime.min.time(),
                        )
                    ),
                    total=found["y"],
                )
            )

    return RiskOverTime(
        should_use_monthly=False if limited_days else weekly_data_size > 12,
        monthly={
            "date": {datum.date: 0 for datum in data_monthly},
            "Closed": {datum.date: datum.closed for datum in data_monthly},
            "Accepted": {datum.date: datum.accepted for datum in data_monthly},
            "Found": {
                datum.date: datum.closed + datum.accepted + datum.opened
                for datum in data_monthly
            },
        },
        weekly={
            "date": {datum.date: 0 for datum in data},
            "Closed": {datum.date: datum.closed for datum in data},
            "Accepted": {datum.date: datum.accepted for datum in data},
            "Found": {
                datum.date: datum.closed + datum.accepted + datum.opened
                for datum in data
            },
        },
    )
