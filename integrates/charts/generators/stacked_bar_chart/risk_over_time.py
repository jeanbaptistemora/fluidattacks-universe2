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
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
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
    loaders: Dataloaders = get_new_context()
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_indicators_typed.load(group)
    )

    if days == 30:
        group_data = group_indicators.remediated_over_time_30 or []
    elif days == 90:
        group_data = group_indicators.remediated_over_time_90 or []
    else:
        group_data = group_indicators.remediated_over_time or []

    group_over_time = [elements[-12:] for elements in group_data]
    group_over_time_monthly = group_indicators.remediated_over_time_month or []
    group_over_time_yearly = group_indicators.remediated_over_time_year or []

    return get_data_risk_over_time_group(
        over_time_weekly=group_over_time,
        over_time_monthly=group_over_time_monthly,
        over_time_yearly=group_over_time_yearly,
        weekly_data_size=len(group_data[0]) if group_data else 0,
        limited_days=bool(days),
    )


async def get_many_groups_document(
    groups: Iterable[str], days: Optional[int] = None
) -> Dict[str, Dict[datetime, float]]:
    group_documents: Tuple[RiskOverTime, ...] = await collect(
        tuple(get_group_document(group, days) for group in groups), workers=32
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
