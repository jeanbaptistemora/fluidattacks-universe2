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
from charts.generators.pie_chart.common import (
    format_csv_data,
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
    GroupTreatmentSummary,
    GroupUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from typing import (
    Optional,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_group(
    loaders: Dataloaders,
    group_name: str,
) -> PortfoliosGroupsInfo:
    indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    total_treatment: Optional[
        GroupTreatmentSummary
    ] = indicators.treatment_summary
    return PortfoliosGroupsInfo(
        group_name=group_name,
        value=Decimal(total_treatment.untreated if total_treatment else 0),
    )


async def get_data_groups(
    loaders: Dataloaders,
    group_names: tuple[str, ...],
) -> list[PortfoliosGroupsInfo]:
    groups_data: tuple[PortfoliosGroupsInfo, ...] = await collect(
        [get_data_group(loaders, group_name) for group_name in group_names],
        workers=32,
    )
    accepted_undefined_vulnerabilities = sum(
        group.value for group in groups_data
    )

    return slice_groups(
        groups_data, Decimal(accepted_undefined_vulnerabilities)
    )


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    headers: list[str] = [
        "Group name",
        "Vulnerabilities with Undefined Treatment",
    ]
    async for org_id, _, org_group_names in (
        utils.iterate_organizations_and_groups()
    ):
        document = format_data(
            groups_data=await get_data_groups(loaders, org_group_names),
        )
        utils.json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document, header=headers),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, group_names in await utils.get_portfolios_groups(
            org_name
        ):
            document = format_data(
                groups_data=await get_data_groups(loaders, group_names),
            )
            utils.json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    document=document, header=headers
                ),
            )


if __name__ == "__main__":
    run(generate_all())
