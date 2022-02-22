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
from groups.domain import (
    get_vulnerabilities_with_pending_attacks,
)
from typing import (
    Any,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str, loaders: Any) -> int:

    return await get_vulnerabilities_with_pending_attacks(
        loaders=loaders, group_name=group
    )


async def get_many_groups(groups: Tuple[str, ...], loaders: Any) -> int:
    groups_data = await collect(
        tuple(generate_one(group, loaders) for group in groups), workers=32
    )

    return sum(groups_data)


def format_data(findings_reattack: int) -> dict:
    return {
        "fontSizeRatio": 0.5,
        "text": findings_reattack,
    }


async def generate_all() -> None:
    loaders = get_new_context()
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                findings_reattack=await generate_one(group, loaders)
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                findings_reattack=await get_many_groups(org_groups, loaders),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    findings_reattack=await get_many_groups(
                        tuple(groups), loaders
                    ),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
