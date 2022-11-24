from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.organization_finding_policies.enums import (
    PolicyStateStatus,
)
from db_model.organization_finding_policies.types import (
    OrgFindingPolicy,
    OrgFindingPolicyRequest,
    OrgFindingPolicyState,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
    OrgFindingPolicyMetadata,
    OrgFindingPolicyState as OrgFindingPolicyStateLegacy,
)
from organizations_finding_policies import (
    domain as policies_domain,
)
import pytest

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_by_id() -> None:
    loaders: Dataloaders = get_new_context()
    org_name = "okada"
    finding_policy_id = "8b35ae2a-56a1-4f64-9da7-6a552683bf46"
    assert await loaders.organization_finding_policy.load(
        OrgFindingPolicyRequest(
            organization_name=org_name,
            policy_id=finding_policy_id,
        )
    ) == OrgFindingPolicy(
        id="8b35ae2a-56a1-4f64-9da7-6a552683bf46",
        organization_name="okada",
        name="007. Cross-site request forgery",
        tags=set(),
        state=OrgFindingPolicyState(
            modified_date="2021-04-26T13:37:10+00:00",
            modified_by="test2@test.com",
            status=PolicyStateStatus.APPROVED,
        ),
    )


async def test_get_finding_policies() -> None:
    org_name = "okada"
    org_findings_policies = await policies_domain.get_finding_policies(
        org_name=org_name
    )

    assert org_findings_policies == (
        OrgFindingPolicyItem(
            id="8b35ae2a-56a1-4f64-9da7-6a552683bf46",
            org_name="okada",
            metadata=OrgFindingPolicyMetadata(
                name="007. Cross-site request forgery",
                tags=set(),
            ),
            state=OrgFindingPolicyStateLegacy(
                modified_date="2021-04-26T13:37:10+00:00",
                modified_by="test2@test.com",
                status="APPROVED",
            ),
        ),
    )
