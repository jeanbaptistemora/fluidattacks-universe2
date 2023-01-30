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
    get_new_context,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> int:
    loaders = get_new_context()
    group_findings = await loaders.group_findings.load(group)
    count = len(group_findings)

    return count


async def get_findings_count_many_groups(groups: tuple[str, ...]) -> int:
    groups_findings = await collect(map(generate_one, groups), workers=32)

    return sum(groups_findings)


def format_data(findings_count: int) -> dict:
    return {"fontSizeRatio": 0.5, "text": findings_count}


async def generate_all() -> None:
    title: str = "Total types"
    async for group in utils.iterate_groups():
        document = format_data(
            findings_count=await generate_one(group),
        )
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                header=title, value=str(document["text"])
            ),
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        document = format_data(
            findings_count=await get_findings_count_many_groups(org_groups),
        )
        utils.json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(
                header=title, value=str(document["text"])
            ),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            document = format_data(
                findings_count=await get_findings_count_many_groups(groups),
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
