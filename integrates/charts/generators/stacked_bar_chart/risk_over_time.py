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
    format_document,
    get_current_time_range,
    get_data_risk_over_time_group,
    RISK_OVER_TIME,
    RiskOverTime,
    sum_over_time_many_groups,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from typing import (
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_group_document(group: str, days: int) -> RiskOverTime:
    context = get_new_context()
    group_loader = context.group

    data_name_monthly = "remediated_over_time_month"
    data_name = "remediated_over_time"
    if days == 30:
        data_name = f"{data_name}_30"
    elif days == 90:
        data_name = f"{data_name}_90"

    group_data = await group_loader.load(group)
    group_over_time = [elements[-12:] for elements in group_data[data_name]]
    group_over_time_monthly = [
        elements[-12:] for elements in group_data[data_name_monthly]
    ]

    return get_data_risk_over_time_group(
        over_time_weekly=group_over_time,
        over_time_monthly=group_over_time_monthly,
        weekly_data_size=len(group_data[data_name][0])
        if group_data[data_name]
        else 0,
        limited_days=bool(days),
    )


async def get_many_groups_document(
    groups: Iterable[str], days: Optional[int] = None
) -> Dict[str, Dict[datetime, float]]:
    group_documents: Tuple[RiskOverTime, ...] = await collect(
        [get_group_document(group, days) for group in groups]
    )

    return sum_over_time_many_groups(
        get_current_time_range(group_documents),
        RISK_OVER_TIME,
    )


async def generate_all() -> None:
    y_label: str = "Vulnerabilities"
    list_days: List[int] = [0, 30, 90]
    for days in list_days:
        async for group in utils.iterate_groups():
            group_document: RiskOverTime = await get_group_document(
                group, days
            )
            utils.json_dump(
                document=format_document(
                    document=get_current_time_range([group_document])[0],
                    y_label=y_label,
                ),
                entity="group",
                subject=group + utils.get_subject_days(days),
            )

        async for org_id, _, org_groups in (
            utils.iterate_organizations_and_groups()
        ):
            utils.json_dump(
                document=format_document(
                    document=await get_many_groups_document(org_groups, days),
                    y_label=y_label,
                ),
                entity="organization",
                subject=org_id + utils.get_subject_days(days),
            )

        async for org_id, org_name, _ in (
            utils.iterate_organizations_and_groups()
        ):
            for portfolio, groups in await utils.get_portfolios_groups(
                org_name
            ):
                utils.json_dump(
                    document=format_document(
                        document=await get_many_groups_document(groups, days),
                        y_label=y_label,
                    ),
                    entity="portfolio",
                    subject=f"{org_id}PORTFOLIO#{portfolio}"
                    + utils.get_subject_days(days),
                )


if __name__ == "__main__":
    run(generate_all())
