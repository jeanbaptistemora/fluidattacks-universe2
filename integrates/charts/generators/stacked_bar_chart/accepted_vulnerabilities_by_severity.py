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
from charts.generators.stacked_bar_chart.utils import (
    get_percentage,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
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
    group_findings_loader = context.group_findings
    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]
    finding_severity_levels = [
        get_severity_level(
            findings_domain.get_severity_score(finding.severity)
        )
        for finding in group_findings
    ]

    finding_vulns_loader = context.finding_vulns_nzr_typed
    finding_vulns: Tuple[
        Tuple[Vulnerability, ...], ...
    ] = await finding_vulns_loader.load_many(finding_ids)
    severity_counter: Counter = Counter()
    for severity, vulns in zip(finding_severity_levels, finding_vulns):
        for vuln in vulns:
            if vuln.state.status == VulnerabilityStateStatus.OPEN:
                severity_counter.update([f"{severity}_open"])
                if vuln.treatment and vuln.treatment.status in {
                    VulnerabilityTreatmentStatus.ACCEPTED,
                    VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                }:
                    severity_counter.update([severity])

    return severity_counter


async def get_data_many_groups(groups: List[str]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_percentages(
    values: Dict[str, Decimal]
) -> Tuple[Dict[str, str], ...]:
    if not values:
        max_percentage_values = dict(
            Accepted="",
            Open="",
        )
        percentage_values = dict(
            Accepted="0.0",
            Open="0.0",
        )

        return (percentage_values, max_percentage_values)

    total_bar: Decimal = values["Accepted"] + values["Open"]
    total_bar = total_bar if total_bar > Decimal("0.0") else Decimal("0.1")
    raw_percentages: List[Decimal] = [
        values["Accepted"] / total_bar,
        values["Open"] / total_bar,
    ]
    percentages: List[Decimal] = get_percentage(raw_percentages)
    max_percentages = max(percentages) if max(percentages) else ""
    is_first_value_max: bool = percentages[0] == max_percentages
    is_second_value_max: bool = percentages[1] == max_percentages
    max_percentage_values = dict(
        Accepted=str(percentages[0]) if is_first_value_max else "",
        Open=str(percentages[1])
        if is_second_value_max and not is_first_value_max
        else "",
    )
    percentage_values = dict(
        Accepted=str(percentages[0]),
        Open=str(percentages[1]),
    )

    return (percentage_values, max_percentage_values)


def format_data(data: Counter[str]) -> Dict[str, Any]:
    translations: Dict[str, str] = {
        "critical_severity": "Critical Severity",
        "high_severity": "High Severity",
        "medium_severity": "Medium Severity",
        "low_severity": "Low Severity",
    }
    percentage_values = [
        format_percentages(
            {
                "Accepted": Decimal(data[column]),
                "Open": Decimal(data[f"{column}_open"] - data[column]),
            }
        )
        for column in translations
    ]

    return dict(
        data=dict(
            columns=[
                [
                    "Accepted",
                    *[data[column] for column in translations],
                ],
                [
                    "Open",
                    *[
                        data[f"{column}_open"] - data[column]
                        for column in translations
                    ],
                ],
            ],
            colors={
                "Accepted": TREATMENT.passive,
                "Open": RISK.more_agressive,
            },
            type="bar",
            groups=[
                ["Accepted", "Open"],
            ],
            labels=dict(
                format=dict(
                    Accepted=None,
                ),
            ),
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
                categories=[value for _, value in translations.items()],
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
        percentageValues=dict(
            Accepted=[
                percentage_value[0]["Accepted"]
                for percentage_value in percentage_values
            ],
            Open=[
                percentage_value[0]["Open"]
                for percentage_value in percentage_values
            ],
        ),
        maxPercentageValues=dict(
            Accepted=[
                percentage_value[1]["Accepted"]
                for percentage_value in percentage_values
            ],
            Open=[
                percentage_value[1]["Open"]
                for percentage_value in percentage_values
            ],
        ),
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
