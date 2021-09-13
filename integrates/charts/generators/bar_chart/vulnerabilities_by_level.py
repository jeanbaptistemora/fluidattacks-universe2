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
from context import (
    FI_API_STATUS,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from operator import (
    itemgetter,
)
from typing import (
    Counter,
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    context = get_new_context()
    if FI_API_STATUS == "migration":
        group_findings_new_loader = context.group_findings_new
        group_findings_new: Tuple[
            Finding, ...
        ] = await group_findings_new_loader.load(group.lower())
        finding_ids = [finding.id for finding in group_findings_new]
    else:
        group_findings_loader = context.group_findings
        group_findings_data = await group_findings_loader.load(group.lower())
        finding_ids = [
            finding["finding_id"] for finding in group_findings_data
        ]

    vulnerabilities = await context.finding_vulns_nzr.load_many_chained(
        finding_ids
    )

    return Counter(filter(None, map(itemgetter("severity"), vulnerabilities)))


async def get_data_many_groups(groups: List[str]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


async def generate_all() -> None:
    column: str = "Level"
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_vulnerabilities_by_data(
                counters=await get_data_one_group(group),
                column=column,
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
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
