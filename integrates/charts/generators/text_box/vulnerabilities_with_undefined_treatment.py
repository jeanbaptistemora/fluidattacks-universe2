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
from groups import (
    domain as groups_domain,
)
from typing import (
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> int:
    item = await groups_domain.get_attributes(group, ["total_treatment"])

    return item.get("total_treatment", {}).get("undefined", 0)


async def get_undefined_count_many_groups(groups: Tuple[str, ...]) -> int:
    groups_undefined_vulns = await collect(map(generate_one, list(groups)))

    return sum(groups_undefined_vulns)


def format_data(undefined_count: int) -> dict:
    return {
        "fontSizeRatio": 0.5,
        "text": undefined_count,
    }


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                undefined_count=await generate_one(group),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                undefined_count=await get_undefined_count_many_groups(
                    org_groups
                ),
            ),
            entity="organization",
            subject=org_id,
        )


if __name__ == "__main__":
    run(generate_all())
