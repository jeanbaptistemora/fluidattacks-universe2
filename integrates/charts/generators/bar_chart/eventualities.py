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
    LIMIT,
)
from charts.generators.bar_chart.utils_top_vulnerabilities_by_source import (
    format_max_value,
)
from charts.generators.common.colors import (
    OTHER_COUNT,
)
from charts.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.events.enums import (
    EventStateStatus,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from decimal import (
    Decimal,
)
from operator import (
    attrgetter,
)
from typing import (
    Any,
    List,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders
) -> PortfoliosGroupsInfo:
    events_group: tuple[Event, ...] = await loaders.group_events.load(
        GroupEventsRequest(group_name=group)
    )

    return PortfoliosGroupsInfo(
        group_name=group.lower(),
        value=Decimal(
            len(
                [
                    event
                    for event in events_group
                    if event.state.status != EventStateStatus.SOLVED
                ]
            )
        ),
    )


async def get_data_many_groups(
    *,
    groups: tuple[str, ...],
    loaders: Dataloaders,
) -> List[PortfoliosGroupsInfo]:
    groups_data = await collect(
        tuple(
            get_data_one_group(group=group, loaders=loaders)
            for group in groups
        ),
        workers=32,
    )

    return sorted(groups_data, key=attrgetter("value"), reverse=True)


def format_data(data: List[PortfoliosGroupsInfo]) -> dict[str, Any]:
    limited_data = [group for group in data[:LIMIT] if group.value > 0]

    return dict(
        data=dict(
            columns=[
                ["Unsolved Events"] + [group.value for group in limited_data],
            ],
            colors={
                "Unsolved Events": OTHER_COUNT,
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
                categories=[group.group_name for group in limited_data],
                type="category",
                tick=dict(
                    multiline=False,
                    outer=False,
                    rotate=0,
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
        maxValue=format_max_value(limited_data),
        exposureTrendsByCategories=True,
        keepToltipColor=True,
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        document = format_data(
            data=await get_data_many_groups(groups=org_groups, loaders=loaders)
        )
        utils.json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            document = format_data(
                data=await get_data_many_groups(
                    groups=tuple(groups), loaders=loaders
                ),
            )
            utils.json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(document=document),
            )


if __name__ == "__main__":
    run(generate_all())
