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
from charts.generators.bar_chart.utils import (
    format_csv_data,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.generators.common.colors import (
    TYPES_COUNT,
)
from charts.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
)
from dataloaders import (
    get_new_context,
)
from decimal import (
    Decimal,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from groups import (
    domain as groups_domain,
)
from operator import (
    attrgetter,
)
from typing import (
    List,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> PortfoliosGroupsInfo:
    context = get_new_context()
    open_findings = await groups_domain.get_open_findings(
        context, group.lower()
    )

    return PortfoliosGroupsInfo(
        group_name=group.lower(),
        value=open_findings,
    )


async def get_data_many_groups(
    groups: tuple[str, ...],
) -> List[PortfoliosGroupsInfo]:
    groups_data = await collect(map(get_data_one_group, groups), workers=16)

    return sorted(groups_data, key=attrgetter("value"), reverse=True)


def format_data(all_data: List[PortfoliosGroupsInfo]) -> dict:
    data = [group for group in all_data[:15] if group.value > Decimal("0.0")]

    return dict(
        data=dict(
            columns=[
                ["Open Types of Vulnerabilities"]
                + [group.value for group in data],
            ],
            colors={
                "Open Types of Vulnerabilities": TYPES_COUNT,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            show=False,
        ),
        axis=dict(
            rotated=True,
            x=dict(
                categories=[group.group_name for group in data],
                type="category",
                tick=dict(
                    rotate=0,
                    multiline=False,
                ),
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        barChartYTickFormat=True,
        maxValue=format_max_value(data),
        exposureTrendsByCategories=True,
        keepToltipColor=True,
    )


@utils.retry_on_exceptions(
    default_value=None,
    exceptions=(UnavailabilityError,),
    retry_times=5,
)
async def generate_all() -> None:
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        document = format_data(
            all_data=await get_data_many_groups(org_groups),
        )
        utils.json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document),
        )

    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            document = format_data(
                all_data=await get_data_many_groups(groups),
            )
            utils.json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(document=document),
            )


if __name__ == "__main__":
    run(generate_all())
