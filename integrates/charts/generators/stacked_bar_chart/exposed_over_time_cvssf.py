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
from charts.colors import (
    RISK,
)
from charts.generators.stacked_bar_chart.utils import (
    DATE_FMT,
    EXPOSED_OVER_TIME,
    get_current_time_range,
    get_quarter,
    get_semester,
    get_time_range,
    RiskOverTime,
    sum_over_time_many_groups,
    translate_date,
    translate_date_last,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
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
    data: List[GroupDocumentCvssfData] = []
    data_monthly: List[GroupDocumentCvssfData] = []
    data_yearly: List[GroupDocumentCvssfData] = []
    data_name = "exposed_over_time_cvssf"

    group_data = await loaders.group.load(group)
    group_over_time = [elements[-12:] for elements in group_data[data_name]]
    group_over_time_monthly = group_data["exposed_over_time_month_cvssf"]
    group_over_time_yearly = group_data["exposed_over_time_year_cvssf"]

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
                    low=low["y"],
                    medium=medium["y"],
                    high=high["y"],
                    critical=critical["y"],
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
                    low=low["y"],
                    medium=medium["y"],
                    high=high["y"],
                    critical=critical["y"],
                    data_date=(
                        translate_date_last(low["x"])
                        if translate_date_last(low["x"]) < datetime.now()
                        else datetime.combine(
                            datetime.now(),
                            datetime.min.time(),
                        )
                    ),
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
                    low=low["y"],
                    medium=medium["y"],
                    high=high["y"],
                    critical=critical["y"],
                    data_date=(
                        datetime.strptime(low["x"], DATE_FMT)
                        if datetime.strptime(low["x"], DATE_FMT)
                        < datetime.now()
                        else datetime.combine(
                            datetime.now(),
                            datetime.min.time(),
                        )
                    ),
                )
            )

    weekly_data_size: int = len(
        group_data[data_name][0] if group_data[data_name] else []
    )

    monthly_data_size: int = len(
        group_data["exposed_over_time_month_cvssf"][0]
        if group_data["exposed_over_time_month_cvssf"]
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
) -> Dict[str, Dict[datetime, float]]:
    group_documents: Tuple[RiskOverTime, ...] = await collect(
        [get_group_document(group, loaders) for group in groups]
    )

    return sum_over_time_many_groups(
        get_current_time_range(group_documents),
        EXPOSED_OVER_TIME,
    )


def format_document(
    document: Dict[str, Dict[datetime, float]],
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
            colors=dict(
                Exposure=RISK.more_agressive,
            ),
            type="area-spline",
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
                    text="CVSSF",
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
            r=0,
        ),
        spline=dict(
            interpolation=dict(
                type="monotone",
            ),
        ),
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    async for group in utils.iterate_groups():
        group_document: RiskOverTime = await get_group_document(group, loaders)
        utils.json_dump(
            document=format_document(
                document=get_current_time_range([group_document])[0],
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_document(
                document=await get_many_groups_document(org_groups, loaders),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_document(
                    document=await get_many_groups_document(
                        tuple(groups), loaders
                    ),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
