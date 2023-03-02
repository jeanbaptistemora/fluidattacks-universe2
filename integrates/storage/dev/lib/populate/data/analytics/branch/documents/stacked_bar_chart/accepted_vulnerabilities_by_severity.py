from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.common.colors import (
    RISK,
    TREATMENT,
)
from charts.generators.common.utils import (
    BAR_RATIO_WIDTH,
)
from charts.generators.stacked_bar_chart import (
    format_csv_data,
)
from charts.generators.stacked_bar_chart.utils import (
    get_percentage,
    MIN_PERCENTAGE,
)
from charts.utils import (
    get_portfolios_groups,
    iterate_groups,
    iterate_organizations_and_groups,
    json_dump,
)
from collections import (
    Counter,
)
from dataloaders import (
    get_new_context,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from decimal import (
    Decimal,
)
from findings import (
    domain as findings_domain,
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
    loaders = get_new_context()
    group_findings = await loaders.group_findings.load(group.lower())
    finding_ids = [finding.id for finding in group_findings]
    finding_severity_levels = [
        get_severity_level(
            findings_domain.get_severity_score(finding.severity)
        )
        for finding in group_findings
    ]

    finding_vulns_loader = loaders.finding_vulnerabilities_released_nzr
    finding_vulns = await finding_vulns_loader.load_many(finding_ids)
    severity_counter: Counter = Counter()
    for severity, vulns in zip(finding_severity_levels, finding_vulns):
        for vuln in vulns:
            if vuln.state.status == VulnerabilityStateStatus.VULNERABLE:
                severity_counter.update([f"{severity}_open"])
                if vuln.treatment and vuln.treatment.status in {
                    VulnerabilityTreatmentStatus.ACCEPTED,
                    VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                }:
                    severity_counter.update([severity])

    return severity_counter


async def get_data_many_groups(groups: list[str]) -> Counter[str]:
    groups_data = await collect(map(get_data_one_group, groups), workers=32)

    return sum(groups_data, Counter())


def format_percentages(
    values: dict[str, Decimal]
) -> tuple[dict[str, str], ...]:
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
    raw_percentages: list[Decimal] = [
        values["Accepted"] / total_bar,
        values["Open"] / total_bar,
    ]
    percentages: list[Decimal] = get_percentage(raw_percentages)
    max_percentage_values = dict(
        Accepted=str(percentages[0])
        if percentages[0] >= MIN_PERCENTAGE
        else "",
        Open=str(percentages[1]) if percentages[1] >= MIN_PERCENTAGE else "",
    )
    percentage_values = dict(
        Accepted=str(percentages[0]),
        Open=str(percentages[1]),
    )

    return (percentage_values, max_percentage_values)


def format_data(data: Counter[str]) -> dict:
    translations: dict[str, str] = {
        "critical_severity": "Critical",
        "high_severity": "High",
        "medium_severity": "Medium",
        "low_severity": "Low",
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
                show=False,
            ),
        ),
        axis=dict(
            x=dict(
                categories=[value for _, value in translations.items()],
                type="category",
                tick=dict(multiline=False),
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
                tick=dict(
                    count=2,
                ),
            ),
        ),
        bar=dict(
            width=dict(
                ratio=BAR_RATIO_WIDTH,
            ),
        ),
        centerLabel=True,
        tooltip=dict(
            format=dict(
                value=None,
            ),
        ),
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
        hideXTickLine=True,
        hideYAxisLine=True,
    )


async def generate_all() -> None:
    header: str = "Categories"
    async for group in iterate_groups():
        document = format_data(data=await get_data_one_group(group))
        json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(document=document, header=header),
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        document = format_data(
            data=await get_data_many_groups(list(org_groups)),
        )
        json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document, header=header),
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            document = format_data(
                data=await get_data_many_groups(list(groups)),
            )
            json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(document=document, header=header),
            )


if __name__ == "__main__":
    run(generate_all())
