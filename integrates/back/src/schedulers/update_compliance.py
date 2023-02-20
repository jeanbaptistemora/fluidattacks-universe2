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
    GroupUnreliableIndicators,
    UnfulfilledStandard,
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
from groups import (
    domain as groups_domain,
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
from search.operations import (
    search,
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
        await loaders.finding_vulnerabilities_released_nzr_c.load(
            FindingVulnerabilitiesZrRequest(
                finding_id=finding.id,
                paginate=False,
                state_status=VulnerabilityStateStatus.VULNERABLE,
            )
        )
    )
    return tuple(edge.node for edge in connections.edges)


async def get_closed_old_vulnerabilities_last_week(
    finding: Finding,
) -> int:
    """Return the amount of vulnerabilities that were open before the
    last week and were closed the last week"""
    results = await search(
        after=None,
        must_filters=[
            {"sk": f"FIN#{finding.id}"},
            {"state.status": "CLOSED"},
            {"state.status": "SAFE"},
        ],
        range_filters=[
            {"state.modified_date": {"gte": "now-1w"}},
            {"created_date": {"lt": "now-1w"}},
        ],
        index="vulnerabilities",
        limit=0,
        query=None,
    )
    return results.total


async def get_closed_vulnerabilities(
    loaders: Dataloaders,
    finding: Finding,
) -> tuple[Vulnerability, ...]:
    connections: VulnerabilitiesConnection = (
        await loaders.finding_vulnerabilities_released_nzr_c.load(
            FindingVulnerabilitiesZrRequest(
                finding_id=finding.id,
                paginate=False,
                state_status=VulnerabilityStateStatus.SAFE,
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
    org_groups: list[Group] = await loaders.organization_groups.load(
        organization.id
    )
    findings = await loaders.group_findings.load_many_chained(
        [group.name for group in org_groups]
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
) -> Decimal:
    org_groups: list[Group] = await loaders.organization_groups.load(
        organization.id
    )
    findings = await loaders.group_findings.load_many_chained(
        [group.name for group in org_groups]
    )
    findings_open_vulnerabilities = await collect(
        tuple(
            get_open_vulnerabilities(loaders, finding) for finding in findings
        ),
        workers=100,
    )
    findings_closed_vulnerabilities_last_week = await collect(
        tuple(
            get_closed_old_vulnerabilities_last_week(finding)
            for finding in findings
        ),
        workers=20,
    )
    a_week_ago = datetime_utils.get_now_minus_delta(weeks=1)
    last_week_open_findings: dict[str, Finding] = {}
    for finding, open_vulnerabilities in zip(
        findings, findings_open_vulnerabilities
    ):
        # Do not count vulnerabilities that were created the last week
        if [
            vulnerability
            for vulnerability in open_vulnerabilities
            if vulnerability.created_date < a_week_ago
        ]:
            last_week_open_findings[finding.id] = finding

    for finding, closed_vulnerabilities_last_week in zip(
        findings, findings_closed_vulnerabilities_last_week
    ):
        # Do not count vulnerabilities that were closed within the last week
        if closed_vulnerabilities_last_week:
            last_week_open_findings[finding.id] = finding

    requirements_by_finding = tuple(
        finding.unfulfilled_requirements
        for finding in last_week_open_findings.values()
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
            ).quantize(Decimal("0.01"))
        ).quantize(Decimal("0.01"))
        if all_compliances
        else Decimal("0.0")
    )


async def get_organization_estimated_days_to_full_compliance(
    loaders: Dataloaders,
    organization: Organization,
    vulnerabilities_file: dict[str, Any],
    default_average_minutes_to_remediate_vulnerability: Decimal,
) -> Decimal:
    org_groups: list[Group] = await loaders.organization_groups.load(
        organization.id
    )
    findings = await loaders.group_findings.load_many_chained(
        [group.name for group in org_groups]
    )
    findings_open_vulnerabilities = await collect(
        tuple(
            get_open_vulnerabilities(loaders, finding) for finding in findings
        ),
        workers=100,
    )
    min_time_to_remediate_total = Decimal("0.0")
    for finding, open_vulnerabilities in zip(
        findings, findings_open_vulnerabilities
    ):
        remediation_time = vulnerabilities_file.get(
            finding.title[:3],
            {
                "remediation_time": (
                    default_average_minutes_to_remediate_vulnerability
                )
            },
        )["remediation_time"]
        min_time_to_remediate_total += (
            default_average_minutes_to_remediate_vulnerability
            if remediation_time == "__empty__"
            else Decimal(remediation_time)
        ) * len(open_vulnerabilities)

    minutes_in_a_day = 1440
    return Decimal(min_time_to_remediate_total / minutes_in_a_day).quantize(
        Decimal("0.01")
    )


async def get_organization_standard_compliances(
    loaders: Dataloaders,
    organization: Organization,
    compliance_file: dict[str, Any],
    requirements_file: dict[str, Any],
) -> list[OrganizationStandardCompliance]:
    org_groups: list[Group] = await loaders.organization_groups.load(
        organization.id
    )
    findings = await loaders.group_findings.load_many_chained(
        [group.name for group in org_groups]
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
        finding.unfulfilled_requirements for finding in open_findings
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
                        non_compliance_definitions_by_standard[
                            standard_name
                        ].intersection(set(standard["definitions"]))
                    )
                )
                / len(standard["definitions"])
            ).quantize(Decimal("0.01")),
        )
        for standard_name, standard in compliance_file.items()
    )


async def update_group_standard_fulfillment(
    loaders: Dataloaders,
    group: Group,
    requirements_file: dict[str, Any],
    vulnerabilities_file: dict[str, Any],
) -> None:
    findings = await loaders.group_findings.load(group.name)
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
    non_compliance_requirements_by_standard: defaultdict[
        str, set
    ] = defaultdict(set)
    for requirements in requirements_by_finding:
        for requirement in requirements:
            for reference in requirements_file[requirement]["references"]:
                non_compliance_requirements_by_standard[
                    get_standard_from_reference(reference)
                ].add(requirement)

    unfulfilled_standards: list[UnfulfilledStandard] = [
        UnfulfilledStandard(
            name=standard_name,
            unfulfilled_requirements=sorted(non_compliance_requirements),
        )
        for standard_name, non_compliance_requirements in (
            non_compliance_requirements_by_standard.items()
        )
        if non_compliance_requirements
    ]
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group.name)
    )
    await groups_domain.update_indicators(
        group_name=group.name,
        indicators=group_indicators._replace(
            unfulfilled_standards=unfulfilled_standards
        ),
    )


async def update_groups_standard_fulfillment(
    loaders: Dataloaders,
    organization: Organization,
    requirements_file: dict[str, Any],
    vulnerabilities_file: dict[str, Any],
) -> None:
    org_groups: list[Group] = await loaders.organization_groups.load(
        organization.id
    )
    await collect(
        tuple(
            update_group_standard_fulfillment(
                loaders=loaders,
                group=group,
                requirements_file=requirements_file,
                vulnerabilities_file=vulnerabilities_file,
            )
            for group in org_groups
        ),
    )


async def update_organization_compliance(
    loaders: Dataloaders,
    organization: Organization,
    compliance_file: dict[str, Any],
    requirements_file: dict[str, Any],
    vulnerabilities_file: dict[str, Any],
    default_average_minutes_to_remediate_vulnerability: Decimal,
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
    )
    estimated_days_to_full_compliance = (
        await get_organization_estimated_days_to_full_compliance(
            loaders=loaders,
            organization=organization,
            vulnerabilities_file=vulnerabilities_file,
            default_average_minutes_to_remediate_vulnerability=(
                default_average_minutes_to_remediate_vulnerability
            ),
        )
    )
    standard_compliances = await get_organization_standard_compliances(
        loaders=loaders,
        organization=organization,
        compliance_file=compliance_file,
        requirements_file=requirements_file,
    )
    await orgs_model.update_unreliable_indicators(
        organization_id=organization.id,
        organization_name=organization.name,
        indicators=OrganizationUnreliableIndicators(
            compliance_level=compliance_level,
            compliance_weekly_trend=compliance_weekly_trend,
            estimated_days_to_full_compliance=(
                estimated_days_to_full_compliance
            ),
            standard_compliances=standard_compliances,
        ),
    )
    await update_groups_standard_fulfillment(
        loaders=loaders,
        organization=organization,
        requirements_file=requirements_file,
        vulnerabilities_file=vulnerabilities_file,
    )


async def update_compliance_indicators(
    loaders: Dataloaders,
    organizations: list[Organization],
    compliance_file: dict[str, Any],
) -> None:
    info("Update compliance indicators")
    organizations_unreliable_indicators = (
        await loaders.organization_unreliable_indicators.load_many(
            [organization.id for organization in organizations]
        )
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
    default_average_minutes_to_remediate_vulnerability = mean(
        [
            Decimal(finding["remediation_time"])
            for finding in vulnerabilities_file.values()
            if finding.get("remediation_time", "__empty__") != "__empty__"
        ]
    )
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
                default_average_minutes_to_remediate_vulnerability=(
                    default_average_minutes_to_remediate_vulnerability
                ),
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
