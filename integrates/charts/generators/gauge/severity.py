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
    GRAY_JET,
    RISK,
)
from custom_types import (
    Finding,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decimal import (
    Decimal,
)
from findings.domain import (
    get_open_vulnerabilities,
)
from typing import (
    List,
    NamedTuple,
    Tuple,
)


class MaxSeverity(NamedTuple):
    value: Decimal
    name: str


class Severity(NamedTuple):
    max_open_severity: MaxSeverity
    max_severity_found: MaxSeverity


def get_max_severity_one(findings: List[Finding]) -> Tuple[int, Decimal]:
    max_index, max_value = (
        (-1, Decimal("0.0"))
        if not findings
        else max(
            enumerate(findings),
            key=lambda finding: Decimal(finding[1].get("cvss_temporal", 0.0)),
        )
    )

    return (
        max_index,
        max_value
        if isinstance(max_value, Decimal)
        else Decimal(max_value.get("cvss_temporal", 0.0)).quantize(
            Decimal("0.1")
        ),
    )


def get_max_severity_many(groups: List[Decimal]) -> Tuple[int, Decimal]:
    max_index, max_value = (
        (-1, Decimal("0.0"))
        if not groups
        else max(enumerate(groups), key=lambda group: Decimal(group[1]))
    )

    return (max_index, max_value)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str, loaders: Dataloaders) -> Severity:
    group_findings_loader = loaders.group_findings
    found_group_findings: List[Finding] = await group_findings_loader.load(
        group.lower()
    )

    max_found_index, max_found_value = get_max_severity_one(
        found_group_findings
    )
    open_findings_vulnerabilities = await collect(
        [
            get_open_vulnerabilities(loaders, str(finding["finding_id"]))
            for finding in found_group_findings
        ]
    )
    open_group_findings = [
        finding
        for finding, open_vulnerabilities in zip(
            found_group_findings, open_findings_vulnerabilities
        )
        if open_vulnerabilities > 0
    ]
    max_open_index, max_open_value = get_max_severity_one(open_group_findings)

    return Severity(
        max_open_severity=MaxSeverity(
            value=max_open_value,
            name=(open_group_findings[max_open_index]["title"])
            if max_open_index >= 0
            else "",
        ),
        max_severity_found=MaxSeverity(
            value=max_found_value,
            name=(found_group_findings[max_found_index]["title"])
            if max_found_index >= 0
            else "",
        ),
    )


async def get_data_many_groups(
    groups: List[str], loaders: Dataloaders
) -> Severity:
    groups_data: List[Severity] = await collect(
        [generate_one(group, loaders) for group in groups]
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
        utils.json_dump(
            document=format_data(
                data=await generate_one(group, loaders),
            ),
            entity="group",
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=await get_data_many_groups(list(org_groups), loaders),
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
                    data=await get_data_many_groups(list(groups), loaders),
                ),
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
            )


if __name__ == "__main__":
    run(generate_all())
