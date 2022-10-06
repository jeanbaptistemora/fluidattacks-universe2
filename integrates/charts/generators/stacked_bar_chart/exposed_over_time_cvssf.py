# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts import (
    utils,
)
from charts.generators.common.colors import (
    RISK,
)
from charts.generators.common.utils import (
    get_max_axis,
)
from charts.generators.stacked_bar_chart import (  # type: ignore
    format_csv_data_over_time,
)
from charts.generators.stacked_bar_chart.utils import (
    DATE_SHORT_FMT,
    DATE_WEEKLY_FMT,
    EXPOSED_OVER_TIME,
    get_current_time_range,
    get_min_date_formatted,
    get_min_date_unformatted,
    get_quarter,
    get_semester,
    get_time_range,
    RiskOverTime,
    sum_over_time_many_groups,
    TimeRangeType,
    translate_date,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Tuple,
)


class GroupDocumentCvssfData(NamedTuple):
    data_date: datetime
    low: Decimal
    medium: Decimal
    high: Decimal
    critical: Decimal


def get_rangetime(
    *,
    group_data: Dict[str, Dict[datetime, Decimal]],
    get_time: Callable[[datetime], datetime],
) -> Dict[str, Dict[datetime, Decimal]]:

    return {
        "date": {
            get_time(key): value for key, value in group_data["date"].items()
        },
        "Exposure": {
            get_time(key): value
            for key, value in group_data["Exposure"].items()
        },
    }


@alru_cache(maxsize=None, typed=True)
async def get_group_document(  # pylint: disable=too-many-locals
    group: str, loaders: Dataloaders
) -> RiskOverTime:
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group)
    )
    data: List[GroupDocumentCvssfData] = []
    data_monthly: List[GroupDocumentCvssfData] = []
    data_yearly: List[GroupDocumentCvssfData] = []

    group_over_time = [
        elements[-12:]
        for elements in group_indicators.exposed_over_time_cvssf or []
    ]
    group_over_time_monthly = group_indicators.exposed_over_time_month_cvssf
    group_over_time_yearly = group_indicators.exposed_over_time_year_cvssf

    if group_over_time:
        group_low_over_time = group_over_time[0]
        group_medium_over_time = group_over_time[1]
        group_high_over_time = group_over_time[2]
        group_critical_over_time = group_over_time[3]

        for low, medium, high, critical in zip(
            group_low_over_time,
            group_medium_over_time,
            group_high_over_time,
            group_critical_over_time,
        ):
            data.append(
                GroupDocumentCvssfData(
                    low=low["y"],  # type: ignore
                    medium=medium["y"],  # type: ignore
                    high=high["y"],  # type: ignore
                    critical=critical["y"],  # type: ignore
                    data_date=translate_date(low["x"]),
                )
            )

    if group_over_time_monthly:
        group_low_over_time = group_over_time_monthly[0]
        group_medium_over_time = group_over_time_monthly[1]
        group_high_over_time = group_over_time_monthly[2]
        group_critical_over_time = group_over_time_monthly[3]

        for low, medium, high, critical in zip(
            group_low_over_time,
            group_medium_over_time,
            group_high_over_time,
            group_critical_over_time,
        ):
            data_monthly.append(
                GroupDocumentCvssfData(
                    low=low["y"],  # type: ignore
                    medium=medium["y"],  # type: ignore
                    high=high["y"],  # type: ignore
                    critical=critical["y"],  # type: ignore
                    data_date=get_min_date_unformatted(low["x"]),
                )
            )

    if group_over_time_yearly:
        group_low_over_time = group_over_time_yearly[0]
        group_medium_over_time = group_over_time_yearly[1]
        group_high_over_time = group_over_time_yearly[2]
        group_critical_over_time = group_over_time_yearly[3]

        for low, medium, high, critical in zip(
            group_low_over_time,
            group_medium_over_time,
            group_high_over_time,
            group_critical_over_time,
        ):
            data_yearly.append(
                GroupDocumentCvssfData(
                    low=low["y"],  # type: ignore
                    medium=medium["y"],  # type: ignore
                    high=high["y"],  # type: ignore
                    critical=critical["y"],  # type: ignore
                    data_date=get_min_date_formatted(low["x"]),
                )
            )

    weekly_data_size: int = len(
        group_indicators.exposed_over_time_cvssf[0]
        if group_indicators.exposed_over_time_cvssf
        else []
    )

    monthly_data_size: int = len(
        group_indicators.exposed_over_time_month_cvssf[0]
        if group_indicators.exposed_over_time_month_cvssf
        else []
    )
    monthly = {
        "date": {datum.data_date: Decimal("0.0") for datum in data_monthly},
        "Exposure": {
            datum.data_date: Decimal(
                datum.low + datum.medium + datum.high + datum.critical
            )
            for datum in data_monthly
        },
    }
    yearly = {
        "date": {datum.data_date: Decimal("0.0") for datum in data_yearly},
        "Exposure": {
            datum.data_date: Decimal(
                datum.low + datum.medium + datum.high + datum.critical
            )
            for datum in data_yearly
        },
    }
    quarterly = get_rangetime(group_data=monthly, get_time=get_quarter)
    semesterly = get_rangetime(group_data=monthly, get_time=get_semester)

    return RiskOverTime(
        time_range=get_time_range(
            weekly_size=weekly_data_size,
            monthly_size=monthly_data_size,
            quarterly_size=len(quarterly["date"]),
            semesterly_size=len(semesterly["date"]),
        ),
        monthly=monthly,
        quarterly=quarterly,
        semesterly=semesterly,
        yearly=yearly,
        weekly={
            "date": {datum.data_date: Decimal("0.0") for datum in data},
            "Exposure": {
                datum.data_date: Decimal(
                    datum.low + datum.medium + datum.high + datum.critical
                )
                for datum in data
            },
        },
    )


async def get_many_groups_document(
    groups: Tuple[str, ...],
    loaders: Dataloaders,
) -> tuple[tuple[dict[str, dict[datetime, float]], ...], TimeRangeType]:
    group_documents: Tuple[RiskOverTime, ...] = await collect(
        tuple(get_group_document(group, loaders) for group in groups),
        workers=32,
    )

    return sum_over_time_many_groups(
        get_current_time_range(group_documents),
        EXPOSED_OVER_TIME,
    )


def format_document(
    data_document: tuple[
        tuple[dict[str, dict[datetime, float]], ...], TimeRangeType
    ],
) -> dict[str, Any]:
    all_documents, time_range = data_document
    document = all_documents[0]

    values: list[Decimal] = [
        utils.format_cvssf(Decimal(document[name][date]))
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
    columns: list[list[str]] = [
        [name]
        + [
            date.strftime(
                DATE_WEEKLY_FMT
                if time_range == TimeRangeType.WEEKLY
                else DATE_SHORT_FMT
            )
            if name == "date"
            else str(utils.format_cvssf(Decimal(document[name][date])))
            for date in tuple(document["date"])[-12:]
        ]
        for name in document
    ]
    return dict(
        data=dict(
            x="date",
            columns=columns,
            colors=dict(
                Exposure=RISK.more_agressive,
            ),
            labels=True,
            type="area",
            groups=[
                [
                    "Exposure",
                ]
            ],
            order=None,
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
                label=dict(
                    text="CVSSF",
                    position="inner-top",
                ),
                min=0,
                padding=dict(
                    bottom=0,
                    top=0,
                ),
                tick=dict(
                    count=5,
                ),
                max=max_axis_value,
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
            show=False,
        ),
        tooltip=dict(
            show=False,
        ),
        point=dict(
            focus=dict(
                expand=dict(
                    enabled=True,
                ),
            ),
            r=3,
        ),
        stackedBarChartYTickFormat=True,
        hideYAxisLine=True,
    )


async def generate_all() -> None:
    header: str = "Dates"
    loaders: Dataloaders = get_new_context()
    async for group in utils.iterate_groups():
        group_document: RiskOverTime = await get_group_document(group, loaders)
        document = format_document(
            data_document=get_current_time_range([group_document]),
        )
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data_over_time(
                document=document, header=header
            ),
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        document = format_document(
            data_document=await get_many_groups_document(org_groups, loaders),
        )
        utils.json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data_over_time(
                document=document, header=header
            ),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            document = format_document(
                data_document=await get_many_groups_document(
                    tuple(groups), loaders
                ),
            )
            utils.json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data_over_time(
                    document=document, header=header
                ),
            )


if __name__ == "__main__":
    run(generate_all())
