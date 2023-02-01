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
from charts.generators.common.colors import (
    GRAY_JET,
    RISK,
)
from charts.generators.gauge.forces_builds_risk import (
    format_csv_data,
)
from dataloaders import (
    Dataloaders,
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
    NamedTuple,
)


class MaxSeverity(NamedTuple):
    value: Decimal
    name: str


class Severity(NamedTuple):
    max_open_severity: MaxSeverity
    max_severity_found: MaxSeverity


def get_max_severity_one(findings: tuple[Finding, ...]) -> tuple[int, Decimal]:
    return max(
        enumerate(
            map(
                findings_domain.get_severity_score,
                [finding.severity for finding in findings],
            )
        ),
        default=(-1, Decimal("0.0")),
        key=lambda enumerated_severity: enumerated_severity[1],
    )


def get_max_severity_many(groups: list[Decimal]) -> tuple[int, Decimal]:
    max_index, max_value = (
        (-1, Decimal("0.0"))
        if not groups
        else max(enumerate(groups), key=lambda group: Decimal(group[1]))
    )

    return (max_index, max_value)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str, loaders: Dataloaders) -> Severity:
    group_findings = await loaders.group_findings.load(group.lower())
    max_found_index, max_found_value = get_max_severity_one(
        tuple(group_findings)
    )
    open_findings_vulnerabilities = await collect(
        tuple(
            findings_domain.get_open_vulnerabilities(loaders, finding.id)
            for finding in group_findings
        ),
        workers=32,
    )
    open_group_findings = tuple(
        finding
        for finding, open_vulnerabilities in zip(
            group_findings, open_findings_vulnerabilities
        )
        if open_vulnerabilities > 0
    )
    max_open_index, max_open_value = get_max_severity_one(open_group_findings)
    severity = Severity(
        max_open_severity=MaxSeverity(
            value=max_open_value,
            name=(open_group_findings[max_open_index].title)
            if max_open_index >= 0
            else "",
        ),
        max_severity_found=MaxSeverity(
            value=max_found_value,
            name=(group_findings[max_found_index].title)
            if max_found_index >= 0
            else "",
        ),
    )
    return severity


async def get_data_many_groups(
    groups: list[str], loaders: Dataloaders
) -> Severity:
    groups_data: tuple[Severity, ...] = await collect(
        tuple(generate_one(group, loaders) for group in groups), workers=32
    )

    max_found_index, max_found_value = get_max_severity_many(
        [group.max_severity_found.value for group in groups_data]
    )
    max_open_index, max_open_value = get_max_severity_many(
        [group.max_open_severity.value for group in groups_data]
    )

    return Severity(
        max_open_severity=MaxSeverity(
            value=max_open_value,
            name=groups[max_open_index].lower() if max_open_index >= 0 else "",
        ),
        max_severity_found=MaxSeverity(
            value=max_found_value,
            name=groups[max_found_index].lower()
            if max_found_index >= 0
            else "",
        ),
    )


def format_data(data: Severity) -> dict:
    return {
        "color": {
            "pattern": [GRAY_JET, RISK.more_agressive],
        },
        "data": {
            "columns": [
                ["Max severity found", data.max_severity_found.value],
                ["Max open severity", data.max_open_severity.value],
            ],
            "names": [
                [data.max_severity_found.name],
                [data.max_open_severity.name],
            ],
            "type": "gauge",
        },
        "gauge": {
            "label": {
                "format": None,
                "show": True,
            },
            "max": 10,
            "min": 0,
        },
        "gaugeClearFormat": True,
        "legend": {
            "position": "right",
        },
        "tooltip": {
            "format": {
                "title": None,
            },
        },
        "formatGaugeTooltip": True,
    }


async def generate_all() -> None:
    loaders = get_new_context()
    async for group in utils.iterate_groups():
        document = format_data(data=await generate_one(group, loaders))
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(document=document),
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        document = format_data(
            data=await get_data_many_groups(list(org_groups), loaders),
        )

        utils.json_dump(
            document=document,
            entity="organization",
            subject=org_id,
            csv_document=format_csv_data(document=document),
        )

    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            document = format_data(
                data=await get_data_many_groups(list(groups), loaders),
            )
            utils.json_dump(
                document=document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=format_csv_data(document=document),
            )


if __name__ == "__main__":
    run(generate_all())
