from aioextensions import (
    collect,
)
from async_lru import (
    alru_cache,
)
from charts import (
    utils,
)
from charts.colors import (
    RISK,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding as FindingNew,
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score_new,
)
from typing import (
    Any,
    Counter,
    Dict,
    List,
    Tuple,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    group: str, loaders: Dataloaders, source: str
) -> Counter[str]:
    findings: Tuple[FindingNew, ...] = await loaders.group_findings_new.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in findings]
    findings_vulns = await loaders.finding_vulns_nzr.load_many(finding_ids)
    findings_cvssf = [
        utils.get_cvssf(get_severity_score_new(finding.severity))
        for finding in findings
    ]

    vulnerabilities_by_source = [
        {finding.title: finding_cvssf}
        for finding, vulnerabilities, finding_cvssf in zip(
            findings, findings_vulns, findings_cvssf
        )
        for vulnerability in vulnerabilities
        if vulnerability["historic_state"][0]["state"] == "open"
        and vulnerability["vuln_type"] == source
    ]

    return sum(
        [Counter(source) for source in vulnerabilities_by_source], Counter()
    )


async def get_data_many_groups(
    groups: Tuple[str, ...],
    loaders: Dataloaders,
    source: str,
) -> Counter[str]:

    groups_data = await collect(
        [get_data_one_group(group, loaders, source) for group in groups]
    )

    return sum(groups_data, Counter())


def format_data(counters: Counter[str], source: str) -> Dict[str, Any]:
    translations = {
        "inputs": "App",
        "lines": "Code",
        "ports": "Infra",
    }
    data: List[Tuple[str, int]] = counters.most_common()[:10]
    legend: str = f"{translations[source]} open severity (CVSSF)"

    return dict(
        data=dict(
            columns=[
                [
                    legend,
                    *[
                        Decimal(value).quantize(Decimal("0.1"))
                        for _, value in data
                    ],
                ],
            ],
            colors={
                legend: RISK.more_agressive,
            },
            type="bar",
        ),
        legend=dict(
            position="bottom",
        ),
        axis=dict(
            x=dict(
                categories=[key for key, _ in data],
                type="category",
                tick=dict(
                    outer=False,
                    rotate=12,
                ),
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
    )


async def generate_all(
    *,
    source: str,
) -> None:
    loaders = get_new_context()
    async for group in iterate_groups():
        json_dump(
            document=format_data(
                await get_data_one_group(group, loaders, source), source
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_dump(
            document=format_data(
                await get_data_many_groups(org_groups, loaders, source), source
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_dump(
                document=format_data(
                    await get_data_many_groups(tuple(groups), loaders, source),
                    source,
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )
