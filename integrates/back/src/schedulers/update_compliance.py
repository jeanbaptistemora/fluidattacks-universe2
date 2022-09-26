# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    organizations as orgs_model,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
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
from typing import (
    Any,
)


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


async def get_organization_non_compliance_level(
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
            len(org_non_compliance.intersection(all_compliances))
            / len(all_compliances)
        ).quantize(Decimal("0.01"))
        if all_compliances
        else Decimal("0.0")
    )


async def update_organization_compliance(
    loaders: Dataloaders,
    organization: Organization,
    compliance_file: dict[str, Any],
    requirements_file: dict[str, Any],
    vulnerabilities_file: dict[str, Any],
) -> None:
    info(f"Working on organization {organization.name}")
    non_compliance_level = await get_organization_non_compliance_level(
        loaders=loaders,
        organization=organization,
        compliance_file=compliance_file,
        requirements_file=requirements_file,
        vulnerabilities_file=vulnerabilities_file,
    )
    info(f"{organization.name} non_compliance_level {non_compliance_level}")
    await orgs_model.update_unreliable_indicators(
        organization_id=organization.id,
        organization_name=organization.name,
        indicators=OrganizationUnreliableIndicators(
            non_compliance_level=non_compliance_level
        ),
    )


async def update_compliance() -> None:
    loaders: Dataloaders = get_new_context()
    compliance_file = await get_compliance_file()
    requirements_file = await get_requirements_file()
    vulnerabilities_file = await get_vulns_file()
    orgs_to_update: list[Organization] = []
    async for organization in orgs_domain.iterate_organizations():
        if orgs_utils.is_deleted(organization):
            continue

        orgs_to_update.append(organization)

    await collect(
        tuple(
            update_organization_compliance(
                loaders=loaders,
                organization=organization,
                compliance_file=compliance_file,
                requirements_file=requirements_file,
                vulnerabilities_file=vulnerabilities_file,
            )
            for organization in orgs_to_update
        ),
        workers=5,
    )


async def main() -> None:
    await update_compliance()
