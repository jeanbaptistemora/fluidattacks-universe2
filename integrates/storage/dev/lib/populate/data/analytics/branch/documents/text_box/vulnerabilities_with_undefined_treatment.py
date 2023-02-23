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
from charts.generators.text_box.utils import (
    format_csv_data,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(
    loaders: Dataloaders,
    group_name: str,
) -> int:
    indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )

    return (
        indicators.treatment_summary.untreated
        if indicators.treatment_summary
        else 0
    )


async def get_undefined_count_many_groups(
    loaders: Dataloaders,
    group_names: tuple[str, ...],
) -> int:
    groups_undefined_vulns = await collect(
        [generate_one(loaders, group_name) for group_name in group_names],
        workers=32,
    )

    return sum(groups_undefined_vulns)


def format_data(undefined_count: int) -> dict:
    return {
        "fontSizeRatio": 0.5,
        "text": undefined_count,
    }


async def generate_all() -> None:
    loaders: Dataloaders = get_new_context()
    title: str = "Vulnerabilities with no treatment"
    async for group_name in utils.iterate_groups():
        document = format_data(
            undefined_count=await generate_one(loaders, group_name),
        )
        utils.json_dump(
            document=document,
            entity="group",
            subject=group_name,
            csv_document=format_csv_data(
                header=title, value=str(document["text"])
            ),
        )

    async for org_id, _, org_group_names in (
        utils.iterate_organizations_and_groups()
    ):
        document = format_data(
            undefined_count=await get_undefined_count_many_groups(
                loaders, org_group_names
            ),
        )
        utils.json_dump(
            entity="organization",
            subject=org_id,
            document=document,
            csv_document=format_csv_data(
                header=title, value=str(document["text"])
            ),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, group_names in await utils.get_portfolios_groups(
            org_name
        ):
            document = format_data(
                undefined_count=await get_undefined_count_many_groups(
                    loaders, group_names
                ),
            )
            utils.json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    header=title, value=str(document["text"])
                ),
            )


if __name__ == "__main__":
    run(generate_all())
