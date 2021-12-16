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
from charts.generators.stacked_bar_chart.utils import (
    DATE_FMT,
    DISTRIBUTION_OVER_TIME,
    format_distribution_document,
    get_current_time_range,
    get_distribution_over_rangetime,
    get_quarter,
    get_semester,
    get_time_range,
    GroupDocumentData,
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
from typing import (
    Dict,
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_group_document(  # pylint: disable=too-many-locals
    group: str,
    loaders: Dataloaders,
) -> RiskOverTime:
    data: List[GroupDocumentData] = []
    data_monthly: List[GroupDocumentData] = []
    data_yearly: List[GroupDocumentData] = []
    data_name = "remediated_over_time"

    group_data = await loaders.group.load(group)
    group_over_time = [elements[-12:] for elements in group_data[data_name]]
    group_over_time_monthly = group_data["remediated_over_time_month"]
    group_over_time_yearly = group_data["remediated_over_time_year"]

    if group_over_time:
        group_opened_over_time = group_over_time[4]
        group_closed_over_time = group_over_time[1]
        group_accepted_over_time = group_over_time[2]

        for accepted, closed, opened in zip(
            group_accepted_over_time,
            group_closed_over_time,
            group_opened_over_time,
        ):
            data.append(
                GroupDocumentData(
                    accepted=accepted["y"],
                    closed=closed["y"],
                    opened=opened["y"],
                    date=translate_date(accepted["x"]),
                    total=opened["y"] + closed["y"] + accepted["y"],
                )
            )

    if group_over_time_monthly:
        group_opened_over_time = group_over_time_monthly[4]
        group_closed_over_time = group_over_time_monthly[1]
        group_accepted_over_time = group_over_time_monthly[2]

        for accepted, closed, opened in zip(
            group_accepted_over_time,
            group_closed_over_time,
            group_opened_over_time,
        ):
            data_monthly.append(
                GroupDocumentData(
                    accepted=accepted["y"],
                    closed=closed["y"],
                    opened=opened["y"],
                    date=(
                        translate_date_last(closed["x"])
                        if translate_date_last(closed["x"]) < datetime.now()
                        else datetime.combine(
                            datetime.now(),
                            datetime.min.time(),
                        )
                    ),
                    total=opened["y"] + closed["y"] + accepted["y"],
                )
            )

    if group_over_time_yearly:
        group_opened_over_time = group_over_time_yearly[4]
        group_closed_over_time = group_over_time_yearly[1]
        group_accepted_over_time = group_over_time_yearly[2]

        for accepted, closed, opened in zip(
            group_accepted_over_time,
            group_closed_over_time,
            group_opened_over_time,
        ):
            data_yearly.append(
                GroupDocumentData(
                    accepted=accepted["y"],
                    closed=closed["y"],
                    opened=opened["y"],
                    date=(
                        datetime.strptime(closed["x"], DATE_FMT)
                        if datetime.strptime(closed["x"], DATE_FMT)
                        < datetime.now()
                        else datetime.combine(
                            datetime.now(),
                            datetime.min.time(),
                        )
                    ),
                    total=opened["y"] + closed["y"] + accepted["y"],
                )
            )

    weekly_data_size: int = len(
        group_data[data_name][0] if group_data[data_name] else []
    )
    monthly_data_size: int = len(
        group_data["remediated_over_time_month"][0]
        if group_data["remediated_over_time_month"]
        else []
    )
    monthly = {
        "date": {datum.date: 0 for datum in data_monthly},
        "Closed": {datum.date: datum.closed for datum in data_monthly},
        "Accepted": {datum.date: datum.accepted for datum in data_monthly},
        "Open": {datum.date: datum.opened for datum in data_monthly},
    }
    quarterly = get_distribution_over_rangetime(
        group_data=monthly, get_time=get_quarter
    )
    semesterly = get_distribution_over_rangetime(
        group_data=monthly, get_time=get_semester
    )
    yearly = {
        "date": {datum.date: 0 for datum in data_yearly},
        "Closed": {datum.date: datum.closed for datum in data_yearly},
        "Accepted": {datum.date: datum.accepted for datum in data_yearly},
        "Open": {datum.date: datum.opened for datum in data_yearly},
    }

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
            "date": {datum.date: 0 for datum in data},
            "Closed": {datum.date: datum.closed for datum in data},
            "Accepted": {datum.date: datum.accepted for datum in data},
            "Open": {datum.date: datum.opened for datum in data},
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
        DISTRIBUTION_OVER_TIME,
    )


async def generate_all() -> None:
    y_label: str = "Vulnerabilities"
    loaders: Dataloaders = get_new_context()
    async for group in utils.iterate_groups():
        group_document: RiskOverTime = await get_group_document(group, loaders)
        utils.json_dump(
            document=format_distribution_document(
                document=get_current_time_range([group_document])[0],
                y_label=y_label,
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_distribution_document(
                document=await get_many_groups_document(org_groups, loaders),
                y_label=y_label,
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_distribution_document(
                    document=await get_many_groups_document(groups, loaders),
                    y_label=y_label,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
