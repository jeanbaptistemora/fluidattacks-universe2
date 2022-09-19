# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    get_closed_vulnerabilities,
    get_open_vulnerabilities,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> int:
    loaders: Dataloaders = get_new_context()
    open_vulnerabilities: int = await get_open_vulnerabilities(loaders, group)
    closed_vulnerabilities: int = await get_closed_vulnerabilities(
        loaders, group
    )

    return closed_vulnerabilities + open_vulnerabilities


async def get_vulns_count_many_groups(groups: tuple[str, ...]) -> int:
    groups_vulns = await collect(map(generate_one, groups), workers=32)

    return sum(groups_vulns)


def format_data(vulns_count: int) -> dict:
    return {
        "fontSizeRatio": 0.5,
        "text": vulns_count,
    }


async def generate_all() -> None:
    header: str = "Total vulnerabilities"
    async for group in utils.iterate_groups():
        document = format_data(
            vulns_count=await generate_one(group),
        )
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                header=header, value=str(document["text"])
            ),
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        document = format_data(
            vulns_count=await get_vulns_count_many_groups(org_groups),
        )
        utils.json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(
                header=header, value=str(document["text"])
            ),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            document = format_data(
                vulns_count=await get_vulns_count_many_groups(groups),
            )
            utils.json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    header=header, value=str(document["text"])
                ),
            )


if __name__ == "__main__":
    run(generate_all())
