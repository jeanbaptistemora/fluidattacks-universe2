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
from groups.domain import (
    get_vulnerabilities_with_pending_attacks,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str, loaders: Dataloaders) -> int:

    return await get_vulnerabilities_with_pending_attacks(
        loaders=loaders, group_name=group
    )


async def get_many_groups(
    groups: tuple[str, ...], loaders: Dataloaders
) -> int:
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
    text = "Vulnerabilities being re-attacked"
    findings_reattack: int
    async for group in utils.iterate_groups():
        findings_reattack = await generate_one(group, loaders)
        utils.json_dump(
            document=format_data(findings_reattack=findings_reattack),
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                header=text, value=str(findings_reattack)
            ),
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        findings_reattack = await get_many_groups(org_groups, loaders)
        utils.json_dump(
            document=format_data(findings_reattack=findings_reattack),
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(
                header=text, value=str(findings_reattack)
            ),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            findings_reattack = await get_many_groups(tuple(groups), loaders)
            utils.json_dump(
                document=format_data(
                    findings_reattack=findings_reattack,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    header=text, value=str(findings_reattack)
                ),
            )


if __name__ == "__main__":
    run(generate_all())
