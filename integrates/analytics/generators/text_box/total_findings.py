# Standard library
from typing import (
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache
from backend.api.dataloaders.project import (
    ProjectLoader as GroupLoader,
)
from backend.api.dataloaders.finding import (
    FindingLoader,
)

# Local libraries
from analytics import (
    utils,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> int:
    findings = (await FindingLoader().load_many(
        (await GroupLoader().load(group))['findings']
    ))

    non_deleted_findings_count = sum(
        1
        for finding in findings
        if 'current_state' in finding
        and finding['current_state'] != 'DELETED'
    )

    return non_deleted_findings_count


async def get_findings_count_many_groups(groups: Tuple[str]) -> int:
    groups_findings = await collect(map(generate_one, list(groups)))

    return sum(groups_findings)


def format_data(findings_count: int) -> dict:
    return {
        'fontSizeRatio': 0.5,
        'text': findings_count
    }


async def generate_all():
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                findings_count=await generate_one(group),
            ),
            entity='group',
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
            entity='organization',
            subject=org_id,
        )


if __name__ == '__main__':
    run(generate_all())
