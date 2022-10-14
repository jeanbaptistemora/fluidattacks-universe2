# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from dataloaders import (
    get_new_context,
)
from db_model.compliance.types import (
    ComplianceStandard,
    ComplianceUnreliableIndicators,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
    UnfulfilledStandard,
)
from db_model.organizations.types import (
    OrganizationStandardCompliance,
    OrganizationUnreliableIndicators,
)
from decimal import (
    Decimal,
)
import pytest
from schedulers import (
    update_compliance,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_compliance")
async def test_update_compliance(populate: bool) -> None:
    assert populate
    await update_compliance.main()

    loaders = get_new_context()
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_indicators: OrganizationUnreliableIndicators = (
        await loaders.organization_unreliable_indicators.load(org_id)
    )
    assert org_indicators == OrganizationUnreliableIndicators(
        compliance_level=Decimal("0.92"),
        compliance_weekly_trend=Decimal("0.00"),
        estimated_days_to_full_compliance=Decimal("0.04"),
        standard_compliances=[
            OrganizationStandardCompliance(
                standard_name="bsimm", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="capec", compliance_level=Decimal("0.78")
            ),
            OrganizationStandardCompliance(
                standard_name="cis", compliance_level=Decimal("0.98")
            ),
            OrganizationStandardCompliance(
                standard_name="cwe", compliance_level=Decimal("0.84")
            ),
            OrganizationStandardCompliance(
                standard_name="eprivacy", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="gdpr", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="hipaa", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="iso27001", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="nerccip", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="nist80053", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="nist80063", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="asvs", compliance_level=Decimal("0.93")
            ),
            OrganizationStandardCompliance(
                standard_name="owasp10", compliance_level=Decimal("0.90")
            ),
            OrganizationStandardCompliance(
                standard_name="pci", compliance_level=Decimal("0.98")
            ),
            OrganizationStandardCompliance(
                standard_name="soc2", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="cwe25", compliance_level=Decimal("0.64")
            ),
            OrganizationStandardCompliance(
                standard_name="owaspm10", compliance_level=Decimal("0.90")
            ),
            OrganizationStandardCompliance(
                standard_name="nist", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="agile", compliance_level=Decimal("0.75")
            ),
            OrganizationStandardCompliance(
                standard_name="bizec", compliance_level=Decimal("0.38")
            ),
            OrganizationStandardCompliance(
                standard_name="ccpa", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="cpra", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="certc", compliance_level=Decimal("0.86")
            ),
            OrganizationStandardCompliance(
                standard_name="certj", compliance_level=Decimal("0.94")
            ),
            OrganizationStandardCompliance(
                standard_name="fcra", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="facta", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="glba", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="misrac", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="nydfs", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="nyshield", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="mitre", compliance_level=Decimal("0.95")
            ),
            OrganizationStandardCompliance(
                standard_name="padss", compliance_level=Decimal("0.95")
            ),
            OrganizationStandardCompliance(
                standard_name="sans25", compliance_level=Decimal("0.72")
            ),
            OrganizationStandardCompliance(
                standard_name="pdpa", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="popia", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="pdpo", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="cmmc", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="hitrust", compliance_level=Decimal("0.98")
            ),
            OrganizationStandardCompliance(
                standard_name="fedramp", compliance_level=Decimal("0.96")
            ),
            OrganizationStandardCompliance(
                standard_name="iso27002", compliance_level=Decimal("0.95")
            ),
            OrganizationStandardCompliance(
                standard_name="lgpd", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="iec62443", compliance_level=Decimal("0.98")
            ),
            OrganizationStandardCompliance(
                standard_name="wassec", compliance_level=Decimal("0.74")
            ),
            OrganizationStandardCompliance(
                standard_name="osstmm3", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="c2m2", compliance_level=Decimal("0.98")
            ),
            OrganizationStandardCompliance(
                standard_name="wasc", compliance_level=Decimal("0.63")
            ),
            OrganizationStandardCompliance(
                standard_name="ferpa", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="nistssdf", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="issaf", compliance_level=Decimal("0.80")
            ),
            OrganizationStandardCompliance(
                standard_name="ptes", compliance_level=Decimal("0.93")
            ),
            OrganizationStandardCompliance(
                standard_name="owasprisks", compliance_level=Decimal("0.94")
            ),
            OrganizationStandardCompliance(
                standard_name="mvsp", compliance_level=Decimal("0.73")
            ),
            OrganizationStandardCompliance(
                standard_name="owaspscp", compliance_level=Decimal("0.71")
            ),
            OrganizationStandardCompliance(
                standard_name="bsafss", compliance_level=Decimal("0.93")
            ),
            OrganizationStandardCompliance(
                standard_name="owaspmasvs", compliance_level=Decimal("0.98")
            ),
            OrganizationStandardCompliance(
                standard_name="nist800171", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="nist800115", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="swiftcsc", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="osamm", compliance_level=Decimal("1.00")
            ),
            OrganizationStandardCompliance(
                standard_name="siglite", compliance_level=Decimal("0.94")
            ),
            OrganizationStandardCompliance(
                standard_name="sig", compliance_level=Decimal("0.97")
            ),
        ],
    )

    compliance_indicators: ComplianceUnreliableIndicators = (
        await loaders.compliance_unreliable_indicators.load("")
    )
    assert compliance_indicators == ComplianceUnreliableIndicators(
        standards=[
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="bsimm",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.78"),
                best_organization_compliance_level=Decimal("0.78"),
                standard_name="capec",
                worst_organization_compliance_level=Decimal("0.78"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.98"),
                best_organization_compliance_level=Decimal("0.98"),
                standard_name="cis",
                worst_organization_compliance_level=Decimal("0.98"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.84"),
                best_organization_compliance_level=Decimal("0.84"),
                standard_name="cwe",
                worst_organization_compliance_level=Decimal("0.84"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="eprivacy",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="gdpr",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="hipaa",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="iso27001",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="nerccip",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="nist80053",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="nist80063",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.93"),
                best_organization_compliance_level=Decimal("0.93"),
                standard_name="asvs",
                worst_organization_compliance_level=Decimal("0.93"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.90"),
                best_organization_compliance_level=Decimal("0.90"),
                standard_name="owasp10",
                worst_organization_compliance_level=Decimal("0.90"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.98"),
                best_organization_compliance_level=Decimal("0.98"),
                standard_name="pci",
                worst_organization_compliance_level=Decimal("0.98"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="soc2",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.64"),
                best_organization_compliance_level=Decimal("0.64"),
                standard_name="cwe25",
                worst_organization_compliance_level=Decimal("0.64"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.90"),
                best_organization_compliance_level=Decimal("0.90"),
                standard_name="owaspm10",
                worst_organization_compliance_level=Decimal("0.90"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="nist",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.75"),
                best_organization_compliance_level=Decimal("0.75"),
                standard_name="agile",
                worst_organization_compliance_level=Decimal("0.75"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.38"),
                best_organization_compliance_level=Decimal("0.38"),
                standard_name="bizec",
                worst_organization_compliance_level=Decimal("0.38"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="ccpa",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="cpra",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.86"),
                best_organization_compliance_level=Decimal("0.86"),
                standard_name="certc",
                worst_organization_compliance_level=Decimal("0.86"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.94"),
                best_organization_compliance_level=Decimal("0.94"),
                standard_name="certj",
                worst_organization_compliance_level=Decimal("0.94"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="fcra",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="facta",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="glba",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="misrac",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="nydfs",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="nyshield",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.95"),
                best_organization_compliance_level=Decimal("0.95"),
                standard_name="mitre",
                worst_organization_compliance_level=Decimal("0.95"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.95"),
                best_organization_compliance_level=Decimal("0.95"),
                standard_name="padss",
                worst_organization_compliance_level=Decimal("0.95"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.72"),
                best_organization_compliance_level=Decimal("0.72"),
                standard_name="sans25",
                worst_organization_compliance_level=Decimal("0.72"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="pdpa",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="popia",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="pdpo",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="cmmc",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.98"),
                best_organization_compliance_level=Decimal("0.98"),
                standard_name="hitrust",
                worst_organization_compliance_level=Decimal("0.98"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.96"),
                best_organization_compliance_level=Decimal("0.96"),
                standard_name="fedramp",
                worst_organization_compliance_level=Decimal("0.96"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.95"),
                best_organization_compliance_level=Decimal("0.95"),
                standard_name="iso27002",
                worst_organization_compliance_level=Decimal("0.95"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="lgpd",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.98"),
                best_organization_compliance_level=Decimal("0.98"),
                standard_name="iec62443",
                worst_organization_compliance_level=Decimal("0.98"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.74"),
                best_organization_compliance_level=Decimal("0.74"),
                standard_name="wassec",
                worst_organization_compliance_level=Decimal("0.74"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="osstmm3",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.98"),
                best_organization_compliance_level=Decimal("0.98"),
                standard_name="c2m2",
                worst_organization_compliance_level=Decimal("0.98"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.63"),
                best_organization_compliance_level=Decimal("0.63"),
                standard_name="wasc",
                worst_organization_compliance_level=Decimal("0.63"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="ferpa",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="nistssdf",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.80"),
                best_organization_compliance_level=Decimal("0.80"),
                standard_name="issaf",
                worst_organization_compliance_level=Decimal("0.80"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.93"),
                best_organization_compliance_level=Decimal("0.93"),
                standard_name="ptes",
                worst_organization_compliance_level=Decimal("0.93"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.94"),
                best_organization_compliance_level=Decimal("0.94"),
                standard_name="owasprisks",
                worst_organization_compliance_level=Decimal("0.94"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.73"),
                best_organization_compliance_level=Decimal("0.73"),
                standard_name="mvsp",
                worst_organization_compliance_level=Decimal("0.73"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.71"),
                best_organization_compliance_level=Decimal("0.71"),
                standard_name="owaspscp",
                worst_organization_compliance_level=Decimal("0.71"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.93"),
                best_organization_compliance_level=Decimal("0.93"),
                standard_name="bsafss",
                worst_organization_compliance_level=Decimal("0.93"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.98"),
                best_organization_compliance_level=Decimal("0.98"),
                standard_name="owaspmasvs",
                worst_organization_compliance_level=Decimal("0.98"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="nist800171",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="nist800115",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="swiftcsc",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("1.00"),
                best_organization_compliance_level=Decimal("1.00"),
                standard_name="osamm",
                worst_organization_compliance_level=Decimal("1.00"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.94"),
                best_organization_compliance_level=Decimal("0.94"),
                standard_name="siglite",
                worst_organization_compliance_level=Decimal("0.94"),
            ),
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.97"),
                best_organization_compliance_level=Decimal("0.97"),
                standard_name="sig",
                worst_organization_compliance_level=Decimal("0.97"),
            ),
        ]
    )

    group_name: str = "group1"
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    assert group_indicators == GroupUnreliableIndicators(
        closed_vulnerabilities=None,
        code_languages=None,
        exposed_over_time_cvssf=None,
        exposed_over_time_month_cvssf=None,
        exposed_over_time_year_cvssf=None,
        last_closed_vulnerability_days=None,
        last_closed_vulnerability_finding=None,
        max_open_severity=None,
        max_open_severity_finding=None,
        max_severity=None,
        mean_remediate=None,
        mean_remediate_critical_severity=None,
        mean_remediate_high_severity=None,
        mean_remediate_low_severity=None,
        mean_remediate_medium_severity=None,
        open_findings=None,
        open_vulnerabilities=None,
        remediated_over_time=None,
        remediated_over_time_30=None,
        remediated_over_time_90=None,
        remediated_over_time_cvssf=None,
        remediated_over_time_cvssf_30=None,
        remediated_over_time_cvssf_90=None,
        remediated_over_time_month=None,
        remediated_over_time_month_cvssf=None,
        remediated_over_time_year=None,
        remediated_over_time_year_cvssf=None,
        treatment_summary=None,
        unfulfilled_standards=[
            UnfulfilledStandard(
                name="capec", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="cwe", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="owasp10", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="agile", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="bizec", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="certj", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="mitre", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="padss", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="sans25", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="wassec", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="wasc", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="issaf", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="ptes", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="owaspscp", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="cwe25", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="asvs", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(
                name="pci", unfulfilled_requirements=["169", "173"]
            ),
            UnfulfilledStandard(name="cis", unfulfilled_requirements=["173"]),
            UnfulfilledStandard(
                name="owaspm10", unfulfilled_requirements=["173"]
            ),
            UnfulfilledStandard(
                name="certc", unfulfilled_requirements=["173"]
            ),
            UnfulfilledStandard(
                name="hitrust", unfulfilled_requirements=["173"]
            ),
            UnfulfilledStandard(
                name="fedramp", unfulfilled_requirements=["173"]
            ),
            UnfulfilledStandard(
                name="iso27002", unfulfilled_requirements=["173"]
            ),
            UnfulfilledStandard(
                name="iec62443", unfulfilled_requirements=["173"]
            ),
            UnfulfilledStandard(
                name="owasprisks", unfulfilled_requirements=["173"]
            ),
            UnfulfilledStandard(name="mvsp", unfulfilled_requirements=["173"]),
            UnfulfilledStandard(
                name="bsafss", unfulfilled_requirements=["173"]
            ),
            UnfulfilledStandard(
                name="owaspmasvs", unfulfilled_requirements=["173"]
            ),
            UnfulfilledStandard(name="c2m2", unfulfilled_requirements=["173"]),
            UnfulfilledStandard(
                name="siglite", unfulfilled_requirements=["173"]
            ),
            UnfulfilledStandard(name="sig", unfulfilled_requirements=["173"]),
        ],
    )
