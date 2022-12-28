from aioextensions import (
    collect,
)
from async_lru import (
    alru_cache,
)
from charts.generators.bar_chart.utils import (
    format_data_csv,
    LIMIT,
)
from charts.generators.common.colors import (
    EXPOSURE,
)
from charts.utils import (
    CsvData,
    format_cvssf,
    format_cvssf_log,
    get_cvssf,
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
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score,
)
from typing import (
    Counter,
)


def format_max_value(data: list[tuple[str, Decimal]]) -> Decimal:
    if data:
        return data[0][1] if data[0][1] else Decimal("1.0")
    return Decimal("1.0")


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(
    group: str, loaders: Dataloaders, source: VulnerabilityType
) -> Counter[str]:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in findings]
    findings_vulns: tuple[
        tuple[Vulnerability, ...], ...
    ] = await loaders.finding_vulnerabilities_released_nzr.load_many(
        finding_ids
    )
    findings_cvssf = [
        get_cvssf(get_severity_score(finding.severity)) for finding in findings
    ]

    vulnerabilities_by_source = [
        {finding.title: finding_cvssf}
        for finding, vulnerabilities, finding_cvssf in zip(
            findings, findings_vulns, findings_cvssf
        )
        for vulnerability in vulnerabilities
        if vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
        and vulnerability.type == source
    ]

    return sum(
        [Counter(source) for source in vulnerabilities_by_source], Counter()
    )


async def get_data_many_groups(
    groups: tuple[str, ...],
    loaders: Dataloaders,
    source: VulnerabilityType,
) -> Counter[str]:

    groups_data = await collect(
        tuple(get_data_one_group(group, loaders, source) for group in groups),
        workers=32,
    )

    return sum(groups_data, Counter())


def format_data(
    counters: Counter[str], source: VulnerabilityType
) -> tuple[dict, CsvData]:
    translations = {
        VulnerabilityType.INPUTS: "App",
        VulnerabilityType.LINES: "Code",
        VulnerabilityType.PORTS: "Infra",
    }
    all_data: list[tuple[str, int]] = counters.most_common()
    data = all_data[:LIMIT]
    legend: str = f"{translations[source]} open exposure"

    json_data = dict(
        data=dict(
            columns=[
                [
                    legend,
                    *[format_cvssf_log(Decimal(value)) for _, value in data],
                ],
            ],
            colors={
                legend: EXPOSURE,
            },
            labels=None,
            type="bar",
        ),
        legend=dict(
            show=False,
        ),
        padding=dict(
            bottom=0,
        ),
        axis=dict(
            rotated=True,
            x=dict(
                categories=[key for key, _ in data],
                type="category",
                tick=dict(
                    multiline=False,
                    outer=False,
                    rotate=0,
                ),
            ),
            y=dict(
                label=dict(
                    text="CVSSF",
                    position="outer-top",
                ),
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        maxValue=format_max_value(
            [(key, Decimal(value)) for key, value in data]
        ),
        maxValueLog=format_max_value(
            [(key, format_cvssf_log(Decimal(value))) for key, value in data]
        ),
        originalValues=[format_cvssf(Decimal(value)) for _, value in data],
        exposureTrendsByCategories=True,
        keepToltipColor=True,
    )

    csv_data = format_data_csv(
        header_value=legend,
        values=[format_cvssf(Decimal(value)) for _, value in all_data],
        categories=[name for name, _ in all_data],
        header_title="Type",
    )

    return (json_data, csv_data)


async def generate_all(
    *,
    source: VulnerabilityType,
) -> None:
    loaders = get_new_context()
    async for group in iterate_groups():
        json_document, csv_document = format_data(
            await get_data_one_group(group, loaders, source), source
        )
        json_dump(
            document=json_document,
            entity="group",
            subject=group,
            csv_document=csv_document,
        )

    async for org_id, _, org_groups in iterate_organizations_and_groups():
        json_document, csv_document = format_data(
            await get_data_many_groups(org_groups, loaders, source), source
        )
        json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in iterate_organizations_and_groups():
        for portfolio, groups in await get_portfolios_groups(org_name):
            json_document, csv_document = format_data(
                await get_data_many_groups(tuple(groups), loaders, source),
                source,
            )
            json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )
