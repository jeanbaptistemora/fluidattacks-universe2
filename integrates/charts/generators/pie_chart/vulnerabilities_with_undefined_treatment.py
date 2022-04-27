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
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_group(
    loaders: Dataloaders,
    group_name: str,
) -> PortfoliosGroupsInfo:
    indicators: GroupUnreliableIndicators = (
        await loaders.group_indicators_typed.load(group_name)
    )
    total_treatment = indicators.treatment_summary
    return PortfoliosGroupsInfo(
        group_name=group_name,
        value=total_treatment.new if total_treatment else 0,
    )


async def get_data_groups(
    loaders: Dataloaders,
    group_names: list[str],
) -> list[PortfoliosGroupsInfo]:
    groups_data: tuple[PortfoliosGroupsInfo, ...] = await collect(
        [get_data_group(loaders, group_name) for group_name in group_names],
        workers=32,
    )
    accepted_undefined_vulnerabilities = sum(
        [group.value for group in groups_data]
    )

    return slice_groups(groups_data, accepted_undefined_vulnerabilities)


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    async for org_id, _, org_group_names in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                groups_data=await get_data_groups(
                    loaders, list(org_group_names)
                ),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, group_names in await utils.get_portfolios_groups(
            org_name
        ):
            utils.json_dump(
                document=format_data(
                    groups_data=await get_data_groups(loaders, group_names),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
