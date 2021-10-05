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
from charts.colors import (
    RISK,
    TREATMENT,
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
from decimal import (
    Decimal,
)
from findings import (
    domain as findings_domain,
)
from typing import (
    Any,
    Counter,
    Dict,
    List,
    Tuple,
)


def get_severity_level(severity: Decimal) -> str:
    if severity <= Decimal("3.9"):
        return "low_severity"
    if 4 <= severity <= Decimal("6.9"):
        return "medium_severity"
    if 7 <= severity <= Decimal("8.9"):
        return "high_severity"

    return "critical_severity"


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter[str]:
    context = get_new_context()
    if FI_API_STATUS == "migration":
        group_findings_new_loader = context.group_findings_new
        group_findings_new: Tuple[
            Finding, ...
        ] = await group_findings_new_loader.load(group.lower())
        finding_ids = [finding.id for finding in group_findings_new]
        finding_severity_levels = [
            get_severity_level(
                findings_domain.get_severity_score_new(finding.severity)
            )
            for finding in group_findings_new
        ]
    else:
        group_findings_loader = context.group_findings
        group_findings = await group_findings_loader.load(group.lower())
        finding_ids = [finding["finding_id"] for finding in group_findings]
        finding_severity_levels = [
            get_severity_level(
                Decimal(finding.get("cvss_temporal", "0.0")).quantize(
                    Decimal("0.1")
                )
            )
            for finding in group_findings
        ]

    finding_vulns_loader = context.finding_vulns_nzr
    finding_vulns = await finding_vulns_loader.load_many(finding_ids)
    severity_counter: Counter = Counter()
    for severity, vulns in zip(finding_severity_levels, finding_vulns):
        for vuln in vulns:
            if vuln["current_state"] == "open":
                severity_counter.update([f"{severity}_open"])
                if vuln["historic_treatment"][-1]["treatment"] in {
                    "ACCEPTED",
                    "ACCEPTED_UNDEFINED",
                }:
                    severity_counter.update([severity])

    return severity_counter


async def get_data_many_groups(groups: List[str]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_data(data: Counter[str]) -> Dict[str, Any]:
    translations = {
        "critical_severity": "Critical Severity",
        "high_severity": "High Severity",
        "medium_severity": "Medium Severity",
        "low_severity": "Low Severity",
    }

    return dict(
        data=dict(
            columns=[
                [
                    "# Accepted Vulnerabilities",
                    *[data[column] for column in translations],
                ],
                [
                    "# Open Vulnerabilities",
                    *[
                        data[f"{column}_open"] - data[column]
                        for column in translations
                    ],
                ],
            ],
            colors={
                "# Accepted Vulnerabilities": TREATMENT.passive,
                "# Open Vulnerabilities": RISK.more_agressive,
            },
            type="bar",
            groups=[
                ["# Accepted Vulnerabilities", "# Open Vulnerabilities"],
            ],
            order=None,
            stack=dict(
                normalize=True,
            ),
        ),
        legend=dict(
            position="bottom",
        ),
        grid=dict(
            y=dict(
                show=True,
            ),
        ),
        axis=dict(
            x=dict(
                categories=[translations[column] for column in translations],
                type="category",
                tick=dict(multiline=False),
            ),
        ),
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
        normalizedToolTip=True,
    )


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(data=await get_data_one_group(group)),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=await get_data_many_groups(list(org_groups)),
            ),
            entity="organization",
            subject=org_id,
        )

    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    data=await get_data_many_groups(list(groups)),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
