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
from charts.generators.bar_chart.utils import (
    format_csv_data,
    format_vulnerabilities_by_data,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from itertools import (
    chain,
)
from typing import (
    Counter,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    context = get_new_context()
    group_findings: Tuple[Finding, ...] = await context.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]

    vulnerabilities = (
        await context.finding_vulnerabilities_nzr.load_many_chained(
            finding_ids
        )
    )

    return Counter(
        filter(
            None,
            chain.from_iterable(map(lambda x: x.tags or [], vulnerabilities)),
        )
    )


async def get_data_many_groups(groups: tuple[str, ...]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups), workers=32)

    return sum(groups_data, Counter())


async def generate_all() -> None:
    column: str = "Tag"
    header: str = "Occurrences"
    async for group in utils.iterate_groups():
        document = format_vulnerabilities_by_data(
            counters=await get_data_one_group(group),
            column=column,
            axis_rotated=True,
        )
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(
                document=document, header=column, alternative=header
            ),
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        document = format_vulnerabilities_by_data(
            counters=await get_data_many_groups(org_groups),
            column=column,
            axis_rotated=True,
        )
        utils.json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(
                document=document, header=column, alternative=header
            ),
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            document = format_vulnerabilities_by_data(
                counters=await get_data_many_groups(groups),
                column=column,
                axis_rotated=True,
            )
            utils.json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(
                    document=document, header=column, alternative=header
                ),
            )


if __name__ == "__main__":
    run(generate_all())
