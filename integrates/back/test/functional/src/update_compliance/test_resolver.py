from dataloaders import (
    get_new_context,
)
from db_model.compliance.types import (
    ComplianceUnreliableIndicators,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
)
from db_model.organizations.types import (
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
    assert org_indicators.compliance_level is not None
    assert org_indicators.compliance_level > Decimal("0.0")
    assert org_indicators.estimated_days_to_full_compliance is not None
    assert org_indicators.estimated_days_to_full_compliance > Decimal("0.0")

    assert org_indicators.compliance_weekly_trend is not None
    assert org_indicators.compliance_weekly_trend == Decimal("0.0")
    assert org_indicators.standard_compliances is not None
    assert len(org_indicators.standard_compliances) > 0

    compliance_indicators: ComplianceUnreliableIndicators = (
        await loaders.compliance_unreliable_indicators.load("")
    )
    assert compliance_indicators.standards is not None
    assert len(compliance_indicators.standards) > 0

    group_name: str = "group1"
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    assert group_indicators.unfulfilled_standards is not None
    assert len(group_indicators.unfulfilled_standards) > 0
