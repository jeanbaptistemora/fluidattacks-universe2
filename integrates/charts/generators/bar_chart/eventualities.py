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
from charts.generators.bar_chart.exposed_by_groups import (
    format_max_value,
)
from charts.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
)
from custom_types import (
    Event,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decimal import (
    Decimal,
)
from events.domain import (
    list_group_events,
)
from operator import (
    attrgetter,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    *, group: str, loaders: Dataloaders
) -> PortfoliosGroupsInfo:
    event_ids = await list_group_events(group)
    group_events: Tuple[Event, ...] = await loaders.event.load_many(event_ids)

    return PortfoliosGroupsInfo(
        group_name=group.lower(),
        value=Decimal(
            len(
                [
                    event
                    for event in group_events
                    if event["event_status"].upper() == "CREATED"
                ]
            )
        ),
    )


async def get_data_many_groups(
    *,
    groups: Tuple[str, ...],
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


def format_data(data: List[PortfoliosGroupsInfo]) -> Dict[str, Any]:
    limited_data = data[:18]

    return dict(
        data=dict(
            columns=[
                ["# Unsolved Eventualities"]
                + [group.value for group in limited_data],
            ],
            colors={
                "# Unsolved Eventualities": RISK.neutral,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            position="bottom",
        ),
        axis=dict(
            x=dict(
                categories=[group.group_name for group in data],
                type="category",
                tick=dict(
                    rotate=utils.TICK_ROTATION,
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
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=await get_data_many_groups(
                    groups=org_groups, loaders=loaders
                ),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    data=await get_data_many_groups(
                        groups=tuple(groups), loaders=loaders
                    ),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
