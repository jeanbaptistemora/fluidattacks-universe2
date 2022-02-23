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
from dataloaders import (
    get_new_context,
)
from decimal import (
    Decimal,
)
from typing import (
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> Decimal:
    context = get_new_context()
    group_data = await context.group.load(group)

    return group_data["last_closing_vuln"]


async def get_many_groups(groups: Tuple[str, ...]) -> Decimal:
    groups_data = await collect(map(generate_one, groups), workers=32)

    return min(groups_data) if groups_data else Decimal("Infinity")


def format_data(last_closing_date: Decimal) -> dict:
    return {"fontSizeRatio": 0.5, "text": last_closing_date}


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(last_closing_date=await generate_one(group)),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                last_closing_date=await get_many_groups(org_groups),
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
                    last_closing_date=await get_many_groups(tuple(groups)),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
