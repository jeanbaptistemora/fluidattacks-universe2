# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# pylint: disable=too-many-locals
# pylint: disable = too-many-arguments

from aioextensions import (
    collect,
)
from collections import (
    defaultdict,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    compliance as compliance_model,
    organizations as orgs_model,
)
from db_model.compliance.types import (
    ComplianceStandard,
    ComplianceUnreliableIndicators,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
    OrganizationStandardCompliance,
    OrganizationUnreliableIndicators,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesZrRequest,
    VulnerabilitiesConnection,
    Vulnerability,
)
from decimal import (
    Decimal,
)
from newutils import (
    datetime as datetime_utils,
    organizations as orgs_utils,
)
from newutils.compliance import (
    get_compliance_file,
)
from newutils.findings import (
    get_requirements_file,
    get_vulns_file,
)
from organizations import (
    domain as orgs_domain,
)
from schedulers.common import (
    info,
)
from statistics import (
    mean,
)
from typing import (
    Any,
)


def get_definition_from_reference(reference: str) -> str:
    return reference.split(".", 1)[1]


def get_standard_from_reference(reference: str) -> str:
    return reference.split(".", 1)[0]


async def get_open_vulnerabilities(
    loaders: Dataloaders,
    finding: Finding,
) -> tuple[Vulnerability, ...]:
    connections: VulnerabilitiesConnection = (
        await loaders.finding_vulnerabilities_nzr_c.load(
            FindingVulnerabilitiesZrRequest(
                finding_id=finding.id,
                paginate=False,
                state_status=VulnerabilityStateStatus.OPEN,
            )
        )
    )
    return tuple(edge.node for edge in connections.edges)


async def get_closed_vulnerabilities(
    loaders: Dataloaders,
    finding: Finding,
) -> tuple[Vulnerability, ...]:
    connections: VulnerabilitiesConnection = (
        await loaders.finding_vulnerabilities_nzr_c.load(
            FindingVulnerabilitiesZrRequest(
                finding_id=finding.id,
                paginate=False,
                state_status=VulnerabilityStateStatus.CLOSED,
            )
        )
    )
    return tuple(edge.node for edge in connections.edges)


async def get_organization_compliance_level(
    loaders: Dataloaders,
    organization: Organization,
    compliance_file: dict[str, Any],
    requirements_file: dict[str, Any],
    vulnerabilities_file: dict[str, Any],
) -> Decimal:
    org_groups: tuple[Group, ...] = await loaders.organization_groups.load(
        organization.id
    )
    findings: tuple[
        Finding, ...
    ] = await loaders.group_findings.load_many_chained(
        tuple(group.name for group in org_groups)
    )
    findings_open_vulnerabilities = await collect(
        tuple(
            get_open_vulnerabilities(loaders, finding) for finding in findings
        ),
        workers=100,
    )
    open_findings: list[Finding] = []
    for finding, open_vulnerabilities in zip(
        findings, findings_open_vulnerabilities
    ):
        if open_vulnerabilities:
            open_findings.append(finding)

    requirements_by_finding = tuple(
        vulnerabilities_file.get(finding.title[:3], {"requirements": []})[
            "requirements"
        ]
        for finding in open_findings
    )
    compliances_by_finding = tuple(
        set(
            reference
            for requirement in requirements
            for reference in requirements_file[requirement]["references"]
        )
        for requirements in requirements_by_finding
    )
    org_non_compliance = (
        set.union(*compliances_by_finding) if compliances_by_finding else set()
    )
    all_compliances = set(
        f"{name.lower()}.{definition}"
        for name, standard in compliance_file.items()
        for definition in standard["definitions"]
    )
    return (
        Decimal(
            (
                len(all_compliances)
                - len(org_non_compliance.intersection(all_compliances))
            )
            / len(all_compliances)
        ).quantize(Decimal("0.01"))
        if all_compliances
        else Decimal("0.0")
    )


async def get_organization_compliance_weekly_trend(
    loaders: Dataloaders,
    organization: Organization,
    current_compliance_level: Decimal,
    compliance_file: dict[str, Any],
    requirements_file: dict[str, Any],
    vulnerabilities_file: dict[str, Any],
) -> Decimal:
    org_groups: tuple[Group, ...] = await loaders.organization_groups.load(
        organization.id
    )
    findings: tuple[
        Finding, ...
    ] = await loaders.group_findings.load_many_chained(
        tuple(group.name for group in org_groups)
    )
    findings_open_vulnerabilities = await collect(
        tuple(
            get_open_vulnerabilities(loaders, finding) for finding in findings
        ),
        workers=100,
    )
    findings_closed_vulnerabilities = await collect(
        tuple(
            get_closed_vulnerabilities(loaders, finding)
            for finding in findings
        ),
        workers=100,
    )
    a_week_ago = datetime_utils.get_now_minus_delta(weeks=1)
    last_week_open_findings: list[Finding] = []
    for finding, open_vulnerabilities in zip(
        findings, findings_open_vulnerabilities
    ):
        # Do not count vulnerabilities that were created the last week
        if [
            vulnerability
            for vulnerability in open_vulnerabilities
            if datetime_utils.get_datetime_from_iso_str(
                vulnerability.created_date
            )
            < a_week_ago
        ]:
            last_week_open_findings.append(finding)

    for finding, closed_vulnerabilities in zip(
        findings, findings_closed_vulnerabilities
    ):
        # Do not count vulnerabilities that were closed within the last week
        if [
            vulnerability
            for vulnerability in closed_vulnerabilities
            if datetime_utils.get_datetime_from_iso_str(
                vulnerability.state.modified_date
            )
            > a_week_ago
        ]:
            last_week_open_findings.append(finding)

    requirements_by_finding = tuple(
        vulnerabilities_file.get(finding.title[:3], {"requirements": []})[
            "requirements"
        ]
        for finding in last_week_open_findings
    )
    compliances_by_finding = tuple(
        set(
            reference
            for requirement in requirements
            for reference in requirements_file[requirement]["references"]
        )
        for requirements in requirements_by_finding
    )
    org_non_compliance = (
        set.union(*compliances_by_finding) if compliances_by_finding else set()
    )
    all_compliances = set(
        f"{name.lower()}.{definition}"
        for name, standard in compliance_file.items()
        for definition in standard["definitions"]
    )
    return (
        (
            current_compliance_level
            - Decimal(
                (
                    len(all_compliances)
                    - len(org_non_compliance.intersection(all_compliances))
                )
                / len(all_compliances)
            )
        ).quantize(Decimal("0.01"))
        if all_compliances
        else Decimal("0.0")
    )


async def get_organization_standard_compliances(
    loaders: Dataloaders,
    organization: Organization,
    compliance_file: dict[str, Any],
    requirements_file: dict[str, Any],
    vulnerabilities_file: dict[str, Any],
) -> list[OrganizationStandardCompliance]:
    org_groups: tuple[Group, ...] = await loaders.organization_groups.load(
        organization.id
    )
    findings: tuple[
        Finding, ...
    ] = await loaders.group_findings.load_many_chained(
        tuple(group.name for group in org_groups)
    )
    findings_open_vulnerabilities = await collect(
        tuple(
            get_open_vulnerabilities(loaders, finding) for finding in findings
        ),
        workers=100,
    )
    open_findings: list[Finding] = []
    for finding, open_vulnerabilities in zip(
        findings, findings_open_vulnerabilities
    ):
        if open_vulnerabilities:
            open_findings.append(finding)

    requirements_by_finding = tuple(
        vulnerabilities_file.get(finding.title[:3], {"requirements": []})[
            "requirements"
        ]
        for finding in open_findings
    )
    non_compliance_definitions_by_standard = defaultdict(set)
    for requirements in requirements_by_finding:
        for requirement in requirements:
            for reference in requirements_file[requirement]["references"]:
                non_compliance_definitions_by_standard[
                    get_standard_from_reference(reference)
                ].add(get_definition_from_reference(reference))

    return list(
        OrganizationStandardCompliance(
            standard_name=standard_name.lower(),
            compliance_level=Decimal(
                (
                    len(standard["definitions"])
                    - len(
                        non_compliance_definitions_by_standard[standard_name]
                    )
                )
                / len(standard["definitions"])
            ).quantize(Decimal("0.01")),
        )
        for standard_name, standard in compliance_file.items()
    )


async def update_organization_compliance(
    loaders: Dataloaders,
    organization: Organization,
    compliance_file: dict[str, Any],
    requirements_file: dict[str, Any],
    vulnerabilities_file: dict[str, Any],
) -> None:
    info(f"Update organization compliance: {organization.name}")
    compliance_level = await get_organization_compliance_level(
        loaders=loaders,
        organization=organization,
        compliance_file=compliance_file,
        requirements_file=requirements_file,
        vulnerabilities_file=vulnerabilities_file,
    )
    compliance_weekly_trend = await get_organization_compliance_weekly_trend(
        loaders=loaders,
        organization=organization,
        compliance_file=compliance_file,
        current_compliance_level=compliance_level,
        requirements_file=requirements_file,
        vulnerabilities_file=vulnerabilities_file,
    )
    standard_compliances = await get_organization_standard_compliances(
        loaders=loaders,
        organization=organization,
        compliance_file=compliance_file,
        requirements_file=requirements_file,
        vulnerabilities_file=vulnerabilities_file,
    )
    await orgs_model.update_unreliable_indicators(
        organization_id=organization.id,
        organization_name=organization.name,
        indicators=OrganizationUnreliableIndicators(
            compliance_level=compliance_level,
            compliance_weekly_trend=compliance_weekly_trend,
            standard_compliances=standard_compliances,
        ),
    )


async def update_compliance_indicators(
    loaders: Dataloaders,
    organizations: list[Organization],
    compliance_file: dict[str, Any],
) -> None:
    info("Update compliance indicators")
    organizations_unreliable_indicators: tuple[
        OrganizationUnreliableIndicators, ...
    ] = await loaders.organization_unreliable_indicators.load_many(
        tuple(organization.id for organization in organizations)
    )
    compliances_level_by_standard: dict[str, set] = {}
    standard_names = tuple(
        standard_name.lower() for standard_name in compliance_file
    )
    for standard_name in standard_names:
        compliances_level_by_standard[standard_name] = set()
    for standard_name in standard_names:
        for indicators in organizations_unreliable_indicators:
            compliance = next(
                (
                    standard_compliance
                    for standard_compliance in indicators.standard_compliances
                    or []
                    if standard_compliance.standard_name == standard_name
                ),
                None,
            )
            if compliance:
                compliances_level_by_standard[standard_name].add(
                    compliance.compliance_level
                )

    await compliance_model.update_unreliable_indicators(
        indicators=ComplianceUnreliableIndicators(
            standards=[
                ComplianceStandard(
                    avg_organization_compliance_level=Decimal(
                        mean(compliances_level_by_standard[standard_name])
                    ).quantize(Decimal("0.01")),
                    best_organization_compliance_level=Decimal(
                        max(compliances_level_by_standard[standard_name])
                    ).quantize(Decimal("0.01")),
                    standard_name=standard_name,
                    worst_organization_compliance_level=Decimal(
                        min(compliances_level_by_standard[standard_name])
                    ).quantize(Decimal("0.01")),
                )
                for standard_name in standard_names
            ]
        )
    )


async def update_compliance() -> None:
    loaders: Dataloaders = get_new_context()
    compliance_file = await get_compliance_file()
    requirements_file = await get_requirements_file()
    vulnerabilities_file = await get_vulns_file()
    current_orgs: list[Organization] = []
    async for organization in orgs_domain.iterate_organizations():
        if orgs_utils.is_deleted(organization):
            continue

        current_orgs.append(organization)

    await collect(
        tuple(
            update_organization_compliance(
                loaders=loaders,
                organization=organization,
                compliance_file=compliance_file,
                requirements_file=requirements_file,
                vulnerabilities_file=vulnerabilities_file,
            )
            for organization in current_orgs
        ),
        workers=5,
    )
    await update_compliance_indicators(
        loaders=loaders,
        organizations=current_orgs,
        compliance_file=compliance_file,
    )


async def main() -> None:
    await update_compliance()
