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
    format_vulnerabilities_by_data,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from typing import (
    Counter,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    context = get_new_context()
    group_findings: tuple[Finding, ...] = await context.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]

    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await context.finding_vulnerabilities_released_nzr.load_many_chained(
        finding_ids
    )

    return Counter(
        [
            str(vulnerability.custom_severity)
            for vulnerability in vulnerabilities
            if vulnerability.custom_severity is not None
            and vulnerability.custom_severity >= 0
        ]
    )


async def get_data_many_groups(groups: tuple[str, ...]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups), workers=32)

    return sum(groups_data, Counter())


async def generate_all() -> None:
    column: str = "Level"
    async for group in utils.iterate_groups():
        json_document, csv_document = format_vulnerabilities_by_data(
            counters=await get_data_one_group(group),
            column=column,
        )
        utils.json_dump(
            document=json_document,
            entity="group",
            subject=group,
            csv_document=csv_document,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        json_document, csv_document = format_vulnerabilities_by_data(
            counters=await get_data_many_groups(org_groups),
            column=column,
        )
        utils.json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            json_document, csv_document = format_vulnerabilities_by_data(
                counters=await get_data_many_groups(groups),
                column=column,
            )
            utils.json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )


if __name__ == "__main__":
    run(generate_all())
