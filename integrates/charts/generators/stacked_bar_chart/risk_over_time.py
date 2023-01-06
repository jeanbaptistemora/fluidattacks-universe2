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
from charts.generators.stacked_bar_chart import (
    format_csv_data_over_time,
)
from charts.generators.stacked_bar_chart.utils import (
    format_risk_document,
    get_current_time_range,
    get_data_risk_over_time_group,
    RISK_OVER_TIME,
    RiskOverTime,
    sum_over_time_many_groups,
    TimeRangeType,
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
    Iterable,
    List,
    Optional,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_group_document(group: str, days: int) -> RiskOverTime:
    loaders: Dataloaders = get_new_context()
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group)
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
) -> tuple[tuple[dict[str, dict[datetime, Decimal]], ...], TimeRangeType]:
    group_documents: Tuple[RiskOverTime, ...] = await collect(
        tuple(get_group_document(group, days) for group in groups), workers=32
    )

    return sum_over_time_many_groups(
        get_current_time_range(group_documents),
        RISK_OVER_TIME,
    )


async def generate_all() -> None:
    y_label: str = "Vulnerabilities"
    header: str = "Dates"
    list_days: List[int] = [0, 30, 90]
    for days in list_days:
        async for group in utils.iterate_groups():
            group_document: RiskOverTime = await get_group_document(
                group, days
            )
            document = format_risk_document(
                data_document=get_current_time_range(tuple([group_document])),
                y_label=y_label,
            )
            utils.json_dump(
                document=document,
                entity="group",
                subject=group + utils.get_subject_days(days),
                csv_document=format_csv_data_over_time(
                    document=document, header=header
                ),
            )

        async for org_id, _, org_groups in (
            utils.iterate_organizations_and_groups()
        ):
            document = format_risk_document(
                data_document=await get_many_groups_document(org_groups, days),
                y_label=y_label,
            )
            utils.json_dump(
                document=document,
                entity="organization",
                subject=org_id + utils.get_subject_days(days),
                csv_document=format_csv_data_over_time(
                    document=document, header=header
                ),
            )

        async for org_id, org_name, _ in (
            utils.iterate_organizations_and_groups()
        ):
            for portfolio, groups in await utils.get_portfolios_groups(
                org_name
            ):
                document = format_risk_document(
                    data_document=await get_many_groups_document(groups, days),
                    y_label=y_label,
                )
                utils.json_dump(
                    document=document,
                    entity="portfolio",
                    subject=f"{org_id}PORTFOLIO#{portfolio}"
                    + utils.get_subject_days(days),
                    csv_document=format_csv_data_over_time(
                        document=document, header=header
                    ),
                )


if __name__ == "__main__":
    run(generate_all())
