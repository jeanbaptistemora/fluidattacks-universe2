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
from charts.generators.pie_chart.utils import (
    format_data,
    PortfoliosGroupsInfo,
    slice_groups,
)
from groups import (
    domain as groups_domain,
)
from typing import (
    List,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_group(group: str) -> PortfoliosGroupsInfo:
    item = await groups_domain.get_attributes(group, ["total_treatment"])

    treatment = item.get("total_treatment", {})

    return PortfoliosGroupsInfo(
        group_name=group.lower(),
        value=treatment.get("undefined", 0),
    )


async def get_data_groups(groups: List[str]) -> List[PortfoliosGroupsInfo]:
    groups_data = await collect(map(get_data_group, groups))
    accepted_undefined_vulnerabilities = sum(
        [group.value for group in groups_data]
    )

    return slice_groups(groups_data, accepted_undefined_vulnerabilities)


async def generate_all() -> None:
    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    groups_data=await get_data_groups(groups),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
