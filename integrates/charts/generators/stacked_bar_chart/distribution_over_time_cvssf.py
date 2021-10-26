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
    data_name = "remediated_over_time_cvssf"

    group_data = await loaders.group.load(group)
    group_over_time = [elements[-12:] for elements in group_data[data_name]]
    group_over_time_monthly = group_data["remediated_over_time_month_cvssf"]

    if group_over_time_monthly:
        group_found_over_time = group_over_time_monthly[0]
        group_closed_over_time = group_over_time_monthly[1]
        group_accepted_over_time = group_over_time_monthly[2]

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
                        translate_date_last(found["x"])
                        if translate_date_last(found["x"]) < datetime.now()
                        else datetime.combine(
                            datetime.now(),
                            datetime.min.time(),
                        )
                    ),
                    total=found["y"],
                )
            )

    if group_over_time:
        group_found_over_time = group_over_time[0]
        group_closed_over_time = group_over_time[1]
        group_accepted_over_time = group_over_time[2]

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
                    date=translate_date(accepted["x"]),
                    total=found["y"],
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

    return RiskOverTime(
        time_range=get_time_range(
            weekly_size=weekly_data_size,
            monthly_size=monthly_data_size,
            quarterly_size=len(quarterly["date"]),
        ),
        monthly=monthly,
        quarterly=quarterly,
        semesterly=semesterly,
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
    y_label: str = "CVSSF"
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
                    document=await get_many_groups_document(
                        tuple(groups), loaders
                    ),
                    y_label=y_label,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
