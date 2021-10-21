from charts.colors import (
    RISK,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
    ROUND_FLOOR,
)
from enum import (
    Enum,
)
from pandas import (
    Timestamp,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Set,
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


class TimeRangeType(Enum):
    WEEKLY: str = "WEEKLY"
    MONTHLY: str = "MONTHLY"
    QUARTERLY: str = "QUARTERLY"


class RiskOverTime(NamedTuple):
    monthly: Dict[str, Dict[datetime, float]]
    quarterly: Dict[str, Dict[datetime, float]]
    time_range: TimeRangeType
    weekly: Dict[str, Dict[datetime, float]]


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
    percentage_values: List[Tuple[Dict[str, str], ...]] = [
        format_severity(
            {
                name: Decimal(document[name][date]).quantize(Decimal("0.1"))
                for name in document
                if name != "date"
            }
        )
        for date in tuple(document["date"])[-12:]
    ]

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
            labels=dict(
                format=dict(
                    Closed=None,
                ),
            ),
            order=None,
            type="bar",
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
        percentageValues=dict(
            Closed=[
                percentage_value[0]["Closed"]
                for percentage_value in percentage_values
            ],
            Accepted=[
                percentage_value[0]["Accepted"]
                for percentage_value in percentage_values
            ],
            Open=[
                percentage_value[0]["Open"]
                for percentage_value in percentage_values
            ],
        ),
        maxPercentageValues=dict(
            Closed=[
                percentage_value[1]["Closed"]
                for percentage_value in percentage_values
            ],
            Accepted=[
                percentage_value[1]["Accepted"]
                for percentage_value in percentage_values
            ],
            Open=[
                percentage_value[1]["Open"]
                for percentage_value in percentage_values
            ],
        ),
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


def get_quarter(data_date: datetime) -> datetime:
    quarter_day = Timestamp(data_date).to_period("Q").end_time.date()

    if quarter_day < datetime.now().date():
        return datetime.combine(quarter_day, datetime.min.time())

    return datetime.combine(
        datetime.now(),
        datetime.min.time(),
    )


def get_risk_over_quarterly(
    group_data: Dict[str, Dict[datetime, float]]
) -> Dict[str, Dict[datetime, float]]:

    return {
        "date": {get_quarter(key): 0 for key, _ in group_data["date"].items()},
        "Closed": {
            get_quarter(key): value
            for key, value in group_data["Closed"].items()
        },
        "Accepted": {
            get_quarter(key): value
            for key, value in group_data["Accepted"].items()
        },
        "Found": {
            get_quarter(key): value
            for key, value in group_data["Found"].items()
        },
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

    monthly_data_size: int = len(
        over_time_monthly[0] if over_time_monthly else []
    )
    monthly: Dict[str, Dict[datetime, float]] = {
        "date": {datum.date: 0 for datum in data_monthly},
        "Closed": {datum.date: datum.closed for datum in data_monthly},
        "Accepted": {datum.date: datum.accepted for datum in data_monthly},
        "Found": {
            datum.date: datum.closed + datum.accepted + datum.opened
            for datum in data_monthly
        },
    }

    return RiskOverTime(
        time_range=TimeRangeType.WEEKLY
        if limited_days
        else get_time_range(weekly_data_size, monthly_data_size),
        monthly=monthly,
        quarterly=get_risk_over_quarterly(monthly),
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


def get_time_range(
    weekly_data_size: int, monthly_size: int = 0
) -> TimeRangeType:
    if not monthly_size:
        return (
            TimeRangeType.MONTHLY
            if weekly_data_size > 12
            else TimeRangeType.WEEKLY
        )

    return (
        TimeRangeType.QUARTERLY if monthly_size > 12 else TimeRangeType.MONTHLY
    )


def round_percentage(percentages: List[Decimal], last: int) -> List[Decimal]:
    sum_percentage = sum(percentages)
    if sum_percentage == Decimal("100.0") or sum_percentage == Decimal("0.0"):
        return percentages

    if last < 0:
        return percentages

    new_percentages = [
        percentage + Decimal("1.0") if index == last else percentage
        for index, percentage in enumerate(percentages)
    ]
    return round_percentage(new_percentages, last - 1)


def get_percentage(values: List[Decimal]) -> List[Decimal]:
    percentages = [
        Decimal(value * Decimal("100.0")).to_integral_exact(
            rounding=ROUND_FLOOR
        )
        for value in values
    ]
    return round_percentage(percentages, len(percentages) - 1)


def format_severity(values: Dict[str, Decimal]) -> Tuple[Dict[str, str], ...]:
    if not values:
        max_percentage_values = dict(
            Closed="",
            Accepted="",
            Open="",
        )
        percentage_values = dict(
            Closed="0.0",
            Accepted="0.0",
            Open="0.0",
        )

        return (percentage_values, max_percentage_values)

    total_bar: Decimal = values["Accepted"] + values["Open"] + values["Closed"]
    total_bar = total_bar if total_bar > Decimal("0.0") else Decimal("0.1")
    raw_percentages: List[Decimal] = [
        values["Closed"] / total_bar,
        values["Accepted"] / total_bar,
        values["Open"] / total_bar,
    ]
    percentages: List[Decimal] = get_percentage(raw_percentages)
    max_percentages = max(percentages) if max(percentages) else ""
    is_first_value_max: bool = percentages[0] == max_percentages
    is_second_value_max: bool = percentages[1] == max_percentages
    max_percentage_values = dict(
        Closed=str(percentages[0]) if is_first_value_max else "",
        Accepted=str(percentages[1])
        if is_second_value_max and not is_first_value_max
        else "",
        Open=str(percentages[2])
        if percentages[2] == max_percentages
        and not (is_first_value_max or is_second_value_max)
        else "",
    )
    percentage_values = dict(
        Closed=str(percentages[0]),
        Accepted=str(percentages[1]),
        Open=str(percentages[2]),
    )

    return (percentage_values, max_percentage_values)


def get_current_time_range(
    group_documents: Tuple[RiskOverTime, ...]
) -> Tuple[Dict[str, Dict[datetime, float]], ...]:
    time_range: Set[TimeRangeType] = {
        group.time_range for group in group_documents
    }

    if TimeRangeType.QUARTERLY in time_range:
        return tuple(
            group_document.quarterly for group_document in group_documents
        )
    if TimeRangeType.MONTHLY in time_range:
        return tuple(
            group_document.monthly for group_document in group_documents
        )
    return tuple(group_document.weekly for group_document in group_documents)


def get_distribution_over_quarterly(
    group_data: Dict[str, Dict[datetime, float]]
) -> Dict[str, Dict[datetime, float]]:

    return {
        "date": {get_quarter(key): 0 for key, _ in group_data["date"].items()},
        "Closed": {
            get_quarter(key): value
            for key, value in group_data["Closed"].items()
        },
        "Accepted": {
            get_quarter(key): value
            for key, value in group_data["Accepted"].items()
        },
        "Open": {
            get_quarter(key): value
            for key, value in group_data["Open"].items()
        },
    }
