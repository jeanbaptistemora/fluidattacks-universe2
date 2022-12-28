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
from charts.generators.stacked_bar_chart.utils import (
    AssignedFormatted,
    format_stacked_vulnerabilities_data,
)
from collections import (
    defaultdict,
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
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from typing import (
    Counter,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> dict[str, list[Vulnerability]]:
    loaders: Dataloaders = get_new_context()
    assigned: dict[str, list[Vulnerability]] = defaultdict(list)
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group.lower()
    )
    finding_ids = [finding.id for finding in group_findings]
    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
        finding_ids
    )

    for vulnerability in vulnerabilities:
        if vulnerability.treatment and vulnerability.treatment.assigned:
            assigned[vulnerability.treatment.assigned].append(vulnerability)

    return assigned


async def get_data_many_groups(
    groups: tuple[str, ...],
) -> dict[str, list[Vulnerability]]:
    groups_data: tuple[dict[str, list[Vulnerability]], ...] = await collect(
        map(get_data_one_group, groups), workers=32
    )
    assigned: dict[str, list[Vulnerability]] = defaultdict(list)

    for group in groups_data:
        for user, vulnerabilities in group.items():
            assigned[user].extend(vulnerabilities)

    return assigned


def format_assigned(
    user: str, vulnerabilities: list[Vulnerability]
) -> AssignedFormatted:
    status: Counter[str] = Counter(
        vulnerability.state.status for vulnerability in vulnerabilities
    )

    treatment: Counter[str] = Counter(
        vulnerability.treatment.status
        for vulnerability in vulnerabilities
        if vulnerability.state.status == VulnerabilityStateStatus.VULNERABLE
        and vulnerability.treatment
        and vulnerability.treatment.status
        in {
            VulnerabilityTreatmentStatus.ACCEPTED,
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
        }
    )

    remaining_open: Decimal = Decimal(
        status[VulnerabilityStateStatus.VULNERABLE]
        - treatment[VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED]
        - treatment[VulnerabilityTreatmentStatus.ACCEPTED]
    )

    return AssignedFormatted(
        accepted=treatment[VulnerabilityTreatmentStatus.ACCEPTED],
        accepted_undefined=treatment[
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ],
        closed_vulnerabilities=status[VulnerabilityStateStatus.SAFE],
        open_vulnerabilities=status[VulnerabilityStateStatus.VULNERABLE],
        remaining_open_vulnerabilities=remaining_open
        if remaining_open > Decimal("0.0")
        else Decimal("0.0"),
        user=user,
    )


def format_data(
    assigned_data: dict[str, list[Vulnerability]]
) -> tuple[dict, utils.CsvData]:
    data: tuple[AssignedFormatted, ...] = tuple(
        format_assigned(user, vulnerabilities)
        for user, vulnerabilities in assigned_data.items()
    )
    limited_data = list(
        sorted(
            data,
            key=lambda x: (
                x.open_vulnerabilities
                / (x.closed_vulnerabilities + x.open_vulnerabilities)
                if (x.closed_vulnerabilities + x.open_vulnerabilities) > 0
                else 0
            ),
            reverse=True,
        )
    )

    return format_stacked_vulnerabilities_data(all_data=limited_data)


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        json_document, csv_document = format_data(
            assigned_data=await get_data_one_group(group)
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
        json_document, csv_document = format_data(
            assigned_data=await get_data_many_groups(org_groups)
        )
        utils.json_dump(
            document=json_document,
            entity="organization",
            subject=org_id,
            csv_document=csv_document,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            json_document, csv_document = format_data(
                assigned_data=await get_data_many_groups(groups)
            )
            utils.json_dump(
                document=json_document,
                entity="portfolio",
                subject=f"{org_id}PORTFOLIO#{portfolio}",
                csv_document=csv_document,
            )


if __name__ == "__main__":
    run(generate_all())
