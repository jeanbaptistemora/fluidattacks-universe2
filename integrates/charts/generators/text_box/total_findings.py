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
from db_model.findings.types import (
    Finding,
)
from typing import (
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> int:
    context = get_new_context()
    group_findings_new_loader = context.group_findings_new
    group_findings_new: Tuple[
        Finding, ...
    ] = await group_findings_new_loader.load(group)
    count = len(group_findings_new)
    return count


async def get_findings_count_many_groups(groups: Tuple[str, ...]) -> int:
    groups_findings = await collect(map(generate_one, list(groups)))

    return sum(groups_findings)


def format_data(findings_count: int) -> dict:
    return {"fontSizeRatio": 0.5, "text": findings_count}


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                findings_count=await generate_one(group),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                findings_count=await get_findings_count_many_groups(
                    org_groups
                ),
            ),
            entity="organization",
            subject=org_id,
        )


if __name__ == "__main__":
    run(generate_all())
