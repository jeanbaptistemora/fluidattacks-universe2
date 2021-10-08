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
from charts.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
)
from dataloaders import (
    get_new_context,
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
    open_findings = await groups_domain.get_open_findings_new(
        context, group.lower()
    )

    return PortfoliosGroupsInfo(
        group_name=group.lower(),
        value=open_findings,
    )


async def get_data_many_groups(
    groups: List[str],
) -> List[PortfoliosGroupsInfo]:
    groups_data = await collect(map(get_data_one_group, groups))

    return sorted(groups_data, key=attrgetter("value"), reverse=True)


def format_data(data: List[PortfoliosGroupsInfo]) -> dict:
    return dict(
        data=dict(
            columns=[
                ["Open Findings"] + [group.value for group in data],
            ],
            colors={
                "Open Findings": RISK.neutral,
            },
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
    )


async def generate_all() -> None:
    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    data=await get_data_many_groups(groups),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
