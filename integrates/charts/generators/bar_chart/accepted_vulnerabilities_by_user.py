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
from typing import (
    Counter,
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    context = get_new_context()
    group_findings: Tuple[Finding, ...] = await context.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]

    vulnerabilities = await context.finding_vulns_nzr.load_many_chained(
        finding_ids
    )

    return Counter(
        [
            vuln["historic_treatment"][-1]["user"]
            for vuln in vulnerabilities
            if vuln["historic_treatment"][-1]["treatment"] == "ACCEPTED"
            and vuln["historic_state"][-1]["state"] == "open"
        ]
    )


async def get_data_many_groups(groups: List[str]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


async def generate_all() -> None:
    column: str = "# Accepted vulnerabilities"
    number_of_categories: int = 10
    tick_rotation: int = 12
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_vulnerabilities_by_data(
                counters=await get_data_one_group(group),
                column=column,
                tick_rotation=tick_rotation,
                categories=number_of_categories,
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_vulnerabilities_by_data(
                counters=await get_data_many_groups(list(org_groups)),
                column=column,
                tick_rotation=tick_rotation,
                categories=number_of_categories,
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_vulnerabilities_by_data(
                    counters=await get_data_many_groups(groups),
                    column=column,
                    tick_rotation=tick_rotation,
                    categories=number_of_categories,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
