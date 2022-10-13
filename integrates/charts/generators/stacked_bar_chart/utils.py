# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint:disable=too-many-lines

from charts.generators.bar_chart.utils import (
    LIMIT,
)
from charts.generators.common.colors import (
    RISK,
    TREATMENT,
)
from charts.generators.common.utils import (
    get_max_axis,
)
from charts.utils import (
    format_cvssf,
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
    Callable,
    Dict,
    List,
    NamedTuple,
    Set,
    Tuple,
)

# Constants
DATE_FMT: str = "%Y - %m - %d"
DATE_SHORT_FMT: str = "%Y-%m"
DATE_WEEKLY_FMT: str = "%y-%m-%d"
MIN_PERCENTAGE: Decimal = Decimal("15.0")
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
    "Reported",
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
    MONTHLY: str = "MONTHLY"
    QUARTERLY: str = "QUARTERLY"
    SEMESTERLY: str = "SEMESTERLY"
    WEEKLY: str = "WEEKLY"
    YEARLY: str = "YEARLY"


class RiskOverTime(NamedTuple):
    monthly: Dict[str, Dict[datetime, float]]
    quarterly: Dict[str, Dict[datetime, float]]
    semesterly: Dict[str, Dict[datetime, float]]
    time_range: TimeRangeType
    weekly: Dict[str, Dict[datetime, float]]
    yearly: Dict[str, Dict[datetime, float]]


class AssignedFormatted(NamedTuple):
    accepted: Decimal
    accepted_undefined: Decimal
    closed_vulnerabilities: Decimal
    open_vulnerabilities: Decimal
    remaining_open_vulnerabilities: Decimal
    user: str


class RemediatedAccepted(NamedTuple):
    accepted: int
    accepted_undefined: int
    closed_vulnerabilities: int
    group_name: str
    open_vulnerabilities: int
    remaining_open_vulnerabilities: int


class RemediatedStatus(NamedTuple):
    closed_vulnerabilities: int
    group_name: str
    open_vulnerabilities: int


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


def format_risk_document(
    data_document: tuple[
        tuple[dict[str, dict[datetime, float]], ...], TimeRangeType
    ],
    y_label: str,
) -> dict[str, Any]:
    all_documents, time_range = data_document
    document = all_documents[0]
    values: list[Decimal] = [
        format_cvssf(Decimal(document[name][date]))
        for date in tuple(document["date"])[-12:]
        for name in document
        if name != "date"
    ]
    max_value: Decimal = (
        list(
            sorted(
                [abs(value) for value in values],
                reverse=True,
            )
        )[0]
        if values
        else Decimal("0.0")
    )
    max_axis_value: Decimal = (
        get_max_axis(value=max_value)
        if max_value > Decimal("0.0")
        else Decimal("0.0")
    )

    return dict(
        data=dict(
            x="date",
            columns=[
                [name]
                + [
                    date.strftime(
                        DATE_WEEKLY_FMT
                        if time_range == TimeRangeType.WEEKLY
                        else DATE_SHORT_FMT
                    )
                    if name == "date"
                    else str(format_cvssf(Decimal(document[name][date])))
                    for date in tuple(document["date"])[-12:]
                ]
                for name in document
            ],
            colors={
                "Closed": RISK.more_passive,
                "Accepted": TREATMENT.passive,
                "Reported": RISK.more_agressive,
            },
            types={
                "Closed": "line",
                "Accepted": "line",
                "Reported": "line",
            },
        ),
        axis=dict(
            x=dict(
                tick=dict(
                    centered=True,
                    multiline=False,
                    rotate=0,
                ),
                type="category",
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                    top=0,
                ),
                label=dict(
                    text=y_label,
                    position="inner-top",
                ),
                tick=dict(
                    count=5,
                ),
                **(
                    {}
                    if max_axis_value == Decimal("0.0")
                    else dict(max=max_axis_value)
                ),
            ),
        ),
        grid=dict(
            x=dict(
                show=False,
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
        stackedBarChartYTickFormat=True,
        hideYAxisLine=True,
    )


def format_distribution_document(
    data_document: tuple[
        tuple[dict[str, dict[datetime, float]], ...], TimeRangeType
    ],
    y_label: str,
) -> dict[str, Any]:
    all_documents, time_range = data_document
    document = all_documents[0]
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
                    date.strftime(
                        DATE_WEEKLY_FMT
                        if time_range == TimeRangeType.WEEKLY
                        else DATE_SHORT_FMT
                    )
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
                "Accepted": TREATMENT.passive,
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
                    rotate=0,
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
                tick=dict(
                    count=2,
                ),
            ),
        ),
        hideYAxisLine=True,
        grid=dict(
            x=dict(
                show=False,
            ),
            y=dict(
                show=False,
            ),
        ),
        legend=dict(
            position="bottom",
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
        hideXTickLine=True,
    )


def sum_over_time_many_groups(
    all_group_documents: tuple[
        tuple[dict[str, dict[datetime, float]], ...], TimeRangeType
    ],
    documents_names: List[str],
) -> tuple[tuple[dict[str, dict[datetime, float]], ...], TimeRangeType]:
    group_documents = all_group_documents[0]
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

    return (
        tuple(
            [
                {
                    name: {
                        date: sum(
                            group_document[name].get(date, 0)
                            for group_document in group_documents
                        )
                        for date in all_dates
                    }
                    for name in documents_names
                }
            ]
        ),
        all_group_documents[1],
    )


def get_semester(data_date: datetime) -> datetime:
    if data_date.month > 6:
        semester_day = (
            Timestamp(datetime(data_date.year, 12, data_date.day))
            .to_period("Q")
            .end_time.date()
        )
    else:
        semester_day = (
            Timestamp(datetime(data_date.year, 5, data_date.day))
            .to_period("Q")
            .end_time.date()
        )

    if semester_day < datetime.now().date():
        return datetime.combine(semester_day, datetime.min.time())

    return datetime.combine(
        datetime.now(),
        datetime.min.time(),
    )


def get_quarter(data_date: datetime) -> datetime:
    quarter_day = Timestamp(data_date).to_period("Q").end_time.date()

    if quarter_day < datetime.now().date():
        return datetime.combine(quarter_day, datetime.min.time())

    return datetime.combine(
        datetime.now(),
        datetime.min.time(),
    )


def get_risk_over_rangetime(
    *,
    group_data: Dict[str, Dict[datetime, float]],
    get_time: Callable[[datetime], datetime],
) -> Dict[str, Dict[datetime, float]]:

    return {
        "date": {get_time(key): 0 for key, _ in group_data["date"].items()},
        "Closed": {
            get_time(key): value for key, value in group_data["Closed"].items()
        },
        "Accepted": {
            get_time(key): value
            for key, value in group_data["Accepted"].items()
        },
        "Reported": {
            get_time(key): value
            for key, value in group_data["Reported"].items()
        },
    }


def get_data_risk_over_time_group(
    *,
    over_time_weekly: List[List[Dict[str, float]]],
    over_time_monthly: List[List[Dict[str, float]]],
    over_time_yearly: List[List[Dict[str, float]]],
    weekly_data_size: int,
    limited_days: bool,
) -> RiskOverTime:
    data: List[GroupDocumentData] = []
    data_monthly: List[GroupDocumentData] = []
    data_yearly: List[GroupDocumentData] = []
    if over_time_weekly:
        for accepted, closed, opened in zip(
            over_time_weekly[2],
            over_time_weekly[1],
            over_time_weekly[4],
        ):
            data.append(
                GroupDocumentData(
                    accepted=accepted["y"],
                    closed=closed["y"],
                    opened=opened["y"],
                    date=translate_date(str(accepted["x"])),
                    total=opened["y"] + closed["y"] + accepted["y"],
                )
            )

    if over_time_monthly:
        for accepted, closed, opened in zip(
            over_time_monthly[2],
            over_time_monthly[1],
            over_time_monthly[4],
        ):
            data_monthly.append(
                GroupDocumentData(
                    accepted=accepted["y"],
                    closed=closed["y"],
                    opened=opened["y"],
                    date=get_min_date_unformatted(str(accepted["x"])),
                    total=opened["y"] + closed["y"] + accepted["y"],
                )
            )

    if over_time_yearly:
        for accepted, closed, opened in zip(
            over_time_yearly[2],
            over_time_yearly[1],
            over_time_yearly[4],
        ):
            data_yearly.append(
                GroupDocumentData(
                    accepted=accepted["y"],
                    closed=closed["y"],
                    opened=opened["y"],
                    date=get_min_date_formatted(str(accepted["x"])),
                    total=opened["y"] + closed["y"] + accepted["y"],
                )
            )

    monthly: Dict[str, Dict[datetime, float]] = {
        "date": {datum.date: 0 for datum in data_monthly},
        "Closed": {datum.date: datum.closed for datum in data_monthly},
        "Accepted": {datum.date: datum.accepted for datum in data_monthly},
        "Reported": {
            datum.date: datum.closed + datum.accepted + datum.opened
            for datum in data_monthly
        },
    }
    yearly: Dict[str, Dict[datetime, float]] = {
        "date": {datum.date: 0 for datum in data_yearly},
        "Closed": {datum.date: datum.closed for datum in data_yearly},
        "Accepted": {datum.date: datum.accepted for datum in data_yearly},
        "Reported": {
            datum.date: datum.closed + datum.accepted + datum.opened
            for datum in data_yearly
        },
    }
    quarterly = get_risk_over_rangetime(
        group_data=monthly, get_time=get_quarter
    )

    semesterly = get_risk_over_rangetime(
        group_data=monthly, get_time=get_semester
    )

    return RiskOverTime(
        time_range=get_time_range(
            weekly_size=weekly_data_size,
            monthly_size=len(
                over_time_monthly[0] if over_time_monthly else []
            ),
            quarterly_size=len(quarterly["date"]),
            semesterly_size=len(semesterly["date"]),
            limited_days=limited_days,
        ),
        monthly=monthly,
        quarterly=quarterly,
        semesterly=semesterly,
        weekly={
            "date": {datum.date: 0 for datum in data},
            "Closed": {datum.date: datum.closed for datum in data},
            "Accepted": {datum.date: datum.accepted for datum in data},
            "Reported": {
                datum.date: datum.closed + datum.accepted + datum.opened
                for datum in data
            },
        },
        yearly=yearly,
    )


def get_time_range(
    *,
    weekly_size: int,
    monthly_size: int,
    quarterly_size: int,
    semesterly_size: int,
    limited_days: bool = False,
) -> TimeRangeType:
    if weekly_size <= 12 or limited_days:
        return TimeRangeType.WEEKLY

    if monthly_size <= 12:
        return TimeRangeType.MONTHLY

    if monthly_size <= 36:
        return TimeRangeType.QUARTERLY

    if 12 < quarterly_size < 24:
        return TimeRangeType.SEMESTERLY

    return (
        TimeRangeType.SEMESTERLY
        if semesterly_size <= 12
        else TimeRangeType.YEARLY
    )


def round_percentage(
    percentages: List[Decimal], exact_percentages: List[Decimal], last: int
) -> List[Decimal]:
    sum_percentage = sum(percentages)
    if sum_percentage == Decimal("100.0") or sum_percentage == Decimal("0.0"):
        return percentages

    if last < 0:
        return round_percentage(
            percentages, exact_percentages, len(percentages) - 1
        )

    new_percentages = [
        percentage + Decimal("1.0")
        if index == last
        and Decimal(exact_percentages[index] * Decimal("100.0"))
        >= Decimal("0.5")
        else percentage
        for index, percentage in enumerate(percentages)
    ]
    return round_percentage(new_percentages, exact_percentages, last - 1)


def get_percentage(values: List[Decimal]) -> List[Decimal]:
    percentages = [
        Decimal(value * Decimal("100.0")).to_integral_exact(
            rounding=ROUND_FLOOR
        )
        for value in values
    ]
    return round_percentage(percentages, values, len(percentages) - 1)


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
    max_percentage_values = dict(
        Closed=str(percentages[0]) if percentages[0] >= MIN_PERCENTAGE else "",
        Accepted=str(percentages[1])
        if percentages[1] >= MIN_PERCENTAGE
        else "",
        Open=str(percentages[2]) if percentages[2] >= MIN_PERCENTAGE else "",
    )
    percentage_values = dict(
        Closed=str(percentages[0]),
        Accepted=str(percentages[1]),
        Open=str(percentages[2]),
    )

    return (percentage_values, max_percentage_values)


def get_current_time_range(
    group_documents: tuple[RiskOverTime, ...]
) -> tuple[tuple[dict[str, dict[datetime, float]], ...], TimeRangeType]:
    time_range: Set[TimeRangeType] = {
        group.time_range for group in group_documents
    }

    if TimeRangeType.YEARLY in time_range:
        return (
            tuple(group_document.yearly for group_document in group_documents),
            TimeRangeType.YEARLY,
        )
    if TimeRangeType.SEMESTERLY in time_range:
        return (
            tuple(
                group_document.semesterly for group_document in group_documents
            ),
            TimeRangeType.SEMESTERLY,
        )
    if TimeRangeType.QUARTERLY in time_range:
        return (
            tuple(
                group_document.quarterly for group_document in group_documents
            ),
            TimeRangeType.QUARTERLY,
        )
    if TimeRangeType.MONTHLY in time_range:
        return (
            tuple(
                group_document.monthly for group_document in group_documents
            ),
            TimeRangeType.MONTHLY,
        )

    return (
        tuple(group_document.weekly for group_document in group_documents),
        TimeRangeType.WEEKLY,
    )


def get_distribution_over_rangetime(
    *,
    group_data: Dict[str, Dict[datetime, float]],
    get_time: Callable[[datetime], datetime],
) -> Dict[str, Dict[datetime, float]]:

    return {
        "date": {get_time(key): 0 for key, _ in group_data["date"].items()},
        "Closed": {
            get_time(key): value for key, value in group_data["Closed"].items()
        },
        "Accepted": {
            get_time(key): value
            for key, value in group_data["Accepted"].items()
        },
        "Open": {
            get_time(key): value for key, value in group_data["Open"].items()
        },
    }


def get_min_date_unformatted(date_str: str) -> datetime:
    if translate_date_last(date_str) < datetime.now():
        return translate_date_last(date_str)

    return datetime.combine(
        datetime.now(),
        datetime.min.time(),
    )


def get_min_date_formatted(date_str: str) -> datetime:
    if datetime.strptime(date_str, DATE_FMT) < datetime.now():
        return datetime.strptime(date_str, DATE_FMT)

    return datetime.combine(
        datetime.now(),
        datetime.min.time(),
    )


def format_stacked_percentages(
    *, values: Dict[str, Decimal]
) -> Tuple[Dict[str, str], ...]:
    if not values:
        max_percentage_values = {
            "Closed": "",
            "Temporarily accepted": "",
            "Permanently accepted": "",
            "Open": "",
        }
        percentage_values = {
            "Closed": "0.0",
            "Temporarily accepted": "0.0",
            "Permanently accepted": "0.0",
            "Open": "0.0",
        }

        return (percentage_values, max_percentage_values)

    total_bar: Decimal = (
        values["Closed"]
        + values["Temporarily accepted"]
        + values["Permanently accepted"]
        + values["Open"]
    )
    total_bar = total_bar if total_bar > Decimal("0.0") else Decimal("0.1")
    raw_percentages: List[Decimal] = [
        values["Closed"] / total_bar,
        values["Temporarily accepted"] / total_bar,
        values["Permanently accepted"] / total_bar,
        values["Open"] / total_bar,
    ]
    percentages: List[Decimal] = get_percentage(raw_percentages)
    max_percentage_values = {
        "Closed": str(percentages[0])
        if percentages[0] >= MIN_PERCENTAGE
        else "",
        "Temporarily accepted": str(percentages[1])
        if percentages[1] >= MIN_PERCENTAGE
        else "",
        "Permanently accepted": str(percentages[2])
        if percentages[2] >= MIN_PERCENTAGE
        else "",
        "Open": str(percentages[3])
        if percentages[3] >= MIN_PERCENTAGE
        else "",
    }
    percentage_values = {
        "Closed": str(percentages[0]),
        "Temporarily accepted": str(percentages[1]),
        "Permanently accepted": str(percentages[2]),
        "Open": str(percentages[3]),
    }

    return (percentage_values, max_percentage_values)


def format_stacked_vulnerabilities_data(
    *,
    limited_data: list[AssignedFormatted],
) -> dict[str, Any]:
    percentage_values = [
        format_stacked_percentages(
            values={
                "Closed": Decimal(user.closed_vulnerabilities),
                "Temporarily accepted": Decimal(user.accepted),
                "Permanently accepted": Decimal(user.accepted_undefined),
                "Open": Decimal(user.remaining_open_vulnerabilities),
            }
        )
        for user in limited_data
    ]

    return dict(
        data=dict(
            columns=[
                ["Closed"]
                + [str(user.closed_vulnerabilities) for user in limited_data],
                ["Temporarily accepted"]
                + [str(user.accepted) for user in limited_data],
                ["Permanently accepted"]
                + [str(user.accepted_undefined) for user in limited_data],
                ["Open"]
                + [
                    str(user.remaining_open_vulnerabilities)
                    for user in limited_data
                ],
            ],
            colors={
                "Closed": RISK.more_passive,
                "Temporarily accepted": TREATMENT.passive,
                "Permanently accepted": TREATMENT.more_passive,
                "Open": RISK.more_agressive,
            },
            labels=dict(
                format=dict(
                    Closed=None,
                ),
            ),
            type="bar",
            groups=[
                [
                    "Closed",
                    "Temporarily accepted",
                    "Permanently accepted",
                    "Open",
                ],
            ],
            order=None,
            stack=dict(
                normalize=True,
            ),
        ),
        legend=dict(
            position="bottom",
        ),
        axis=dict(
            rotated=True,
            x=dict(
                categories=[assigned.user for assigned in limited_data],
                type="category",
                tick=dict(rotate=0, multiline=False),
            ),
            y=dict(
                label=dict(
                    position="outer-top",
                ),
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
        percentageValues={
            "Closed": [
                percentage_value[0]["Closed"]
                for percentage_value in percentage_values
            ],
            "Temporarily accepted": [
                percentage_value[0]["Temporarily accepted"]
                for percentage_value in percentage_values
            ],
            "Permanently accepted": [
                percentage_value[0]["Permanently accepted"]
                for percentage_value in percentage_values
            ],
            "Open": [
                percentage_value[0]["Open"]
                for percentage_value in percentage_values
            ],
        },
        maxPercentageValues={
            "Closed": [
                percentage_value[1]["Closed"]
                for percentage_value in percentage_values
            ],
            "Temporarily accepted": [
                percentage_value[1]["Temporarily accepted"]
                for percentage_value in percentage_values
            ],
            "Permanently accepted": [
                percentage_value[1]["Permanently accepted"]
                for percentage_value in percentage_values
            ],
            "Open": [
                percentage_value[1]["Open"]
                for percentage_value in percentage_values
            ],
        },
    )


def limit_data(data: list[RemediatedAccepted]) -> list[RemediatedAccepted]:
    return list(
        sorted(
            [
                group
                for group in data
                if Decimal(
                    Decimal(group.closed_vulnerabilities)
                    + Decimal(group.remaining_open_vulnerabilities)
                    + Decimal(group.accepted)
                    + Decimal(group.accepted_undefined)
                )
                > Decimal("0.0")
            ],
            key=lambda x: (
                x.open_vulnerabilities
                / (x.closed_vulnerabilities + x.open_vulnerabilities)
                if (x.closed_vulnerabilities + x.open_vulnerabilities) > 0
                else 0
            ),
            reverse=True,
        )
    )[:LIMIT]
