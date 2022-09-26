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
from charts.generators.stacked_bar_chart import (  # type: ignore
    format_csv_data_over_time,
)
from charts.generators.stacked_bar_chart.utils import (
    format_document,
    get_current_time_range,
    get_data_risk_over_time_group,
    RISK_OVER_TIME,
    RiskOverTime,
    sum_over_time_many_groups,
)
from charts.utils import (
    get_portfolios_groups,
    get_subject_days,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
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


@alru_cache(maxsize=None, typed=True)
async def get_group_document(group: str, days: int) -> RiskOverTime:
    loaders: Dataloaders = get_new_context()
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group)
    )

    if days == 30:
        group_data = group_indicators.remediated_over_time_cvssf_30 or []
    elif days == 90:
        group_data = group_indicators.remediated_over_time_cvssf_90 or []
    else:
        group_data = group_indicators.remediated_over_time_cvssf or []

    group_over_time = [elements[-12:] for elements in group_data]
    group_over_time_monthly = (
        group_indicators.remediated_over_time_month_cvssf or []
    )
    group_over_time_yearly = (
        group_indicators.remediated_over_time_year_cvssf or []
    )

    return get_data_risk_over_time_group(
        over_time_weekly=group_over_time,
        over_time_monthly=group_over_time_monthly,
        over_time_yearly=group_over_time_yearly,
        weekly_data_size=len(group_data[0]) if group_data else 0,
        limited_days=bool(days),
    )


async def get_many_groups_document(
    groups: tuple[str, ...],
    days: int,
) -> dict[str, dict[datetime, float]]:
    group_documents: tuple[RiskOverTime, ...] = await collect(
        tuple(get_group_document(group, days) for group in groups), workers=32
    )

    return sum_over_time_many_groups(
        get_current_time_range(group_documents),
        RISK_OVER_TIME,
    )


async def generate_all() -> None:
    y_label: str = "CVSSF"
    header: str = "Dates"
    list_days: list[int] = [0, 30, 90]
    for days in list_days:
        async for group in iterate_groups():
            group_document: RiskOverTime = await get_group_document(
                group, days
            )
            document = format_document(
                document=get_current_time_range([group_document])[0],
                y_label=y_label,
            )
            json_dump(
                document=document,
                entity="group",
                subject=group + get_subject_days(days),
                csv_document=format_csv_data_over_time(
                    document=document, header=header
                ),
            )

        async for org_id, _, org_groups in iterate_organizations_and_groups():
            document = format_document(
                document=await get_many_groups_document(org_groups, days),
                y_label=y_label,
            )
            json_dump(
                document=document,
                entity="organization",
                subject=org_id + get_subject_days(days),
                csv_document=format_csv_data_over_time(
                    document=document, header=header
                ),
            )

        async for org_id, org_name, _ in iterate_organizations_and_groups():
            for portfolio, groups in await get_portfolios_groups(org_name):
                document = format_document(
                    document=await get_many_groups_document(groups, days),
                    y_label=y_label,
                )
                json_dump(
                    document=document,
                    entity="portfolio",
                    subject=f"{org_id}PORTFOLIO#{portfolio}"
                    + get_subject_days(days),
                    csv_document=format_csv_data_over_time(
                        document=document, header=header
                    ),
                )


if __name__ == "__main__":
    run(generate_all())
