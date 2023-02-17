from .schema import (
    ORGANIZATION_COMPLIANCE,
)
from .types import (
    OrganizationComplianceStandard,
)
from dataloaders import (
    Dataloaders,
)
from db_model.compliance.types import (
    ComplianceStandard,
    ComplianceUnreliableIndicators,
)
from db_model.organizations.types import (
    OrganizationStandardCompliance,
    OrganizationUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.compliance import (
    get_compliance_file,
)


@ORGANIZATION_COMPLIANCE.field("standards")
async def resolve(
    parent: OrganizationUnreliableIndicators,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[OrganizationComplianceStandard]:
    loaders: Dataloaders = info.context.loaders
    compliance_indicators: ComplianceUnreliableIndicators = (
        await loaders.compliance_unreliable_indicators.load("")
    )
    compliance_file = {
        standard_name.lower(): standard
        for standard_name, standard in (await get_compliance_file()).items()
    }
    org_compliance_by_standard = {
        standard_compliance.standard_name: standard_compliance
        for standard_compliance in parent.standard_compliances or []
    }
    full_org_compliance_by_standard = {
        standard_name: org_compliance_by_standard.get(
            standard_name,
            OrganizationStandardCompliance(
                compliance_level=Decimal("0.0"),
                standard_name=standard_name,
            ),
        )
        for standard_name in compliance_file
    }
    global_compliance_by_standard = {
        compliance_standard.standard_name: compliance_standard
        for compliance_standard in compliance_indicators.standards or []
    }
    full_global_compliance_by_standard = {
        standard_name: global_compliance_by_standard.get(
            standard_name,
            ComplianceStandard(
                avg_organization_compliance_level=Decimal("0.0"),
                best_organization_compliance_level=Decimal("0.0"),
                standard_name=standard_name,
                worst_organization_compliance_level=Decimal("0.0"),
            ),
        )
        for standard_name in compliance_file
    }
    return [
        OrganizationComplianceStandard(
            avg_organization_compliance_level=(
                full_global_compliance_by_standard[standard_id]
            ).avg_organization_compliance_level,
            best_organization_compliance_level=(
                full_global_compliance_by_standard[standard_id]
            ).best_organization_compliance_level,
            compliance_level=(
                full_org_compliance_by_standard[standard_id]
            ).compliance_level,
            standard_id=standard_id,
            standard_title=standard["title"],
            worst_organization_compliance_level=(
                full_global_compliance_by_standard[standard_id]
            ).worst_organization_compliance_level,
        )
        for standard_id, standard in compliance_file.items()
    ]
