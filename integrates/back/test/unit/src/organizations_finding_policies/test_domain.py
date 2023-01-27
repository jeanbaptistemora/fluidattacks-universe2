from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.organization_finding_policies.enums import (
    PolicyStateStatus,
)
from db_model.organization_finding_policies.types import (
    OrgFindingPolicy,
    OrgFindingPolicyRequest,
    OrgFindingPolicyState,
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
        state=OrgFindingPolicyState(
            modified_date=datetime.fromisoformat("2021-04-26T13:37:10+00:00"),
            modified_by="test2@test.com",
            status=PolicyStateStatus.APPROVED,
        ),
        tags=set(),
    )


async def test_get_finding_policies_by_org_name() -> None:
    loaders: Dataloaders = get_new_context()
    org_name = "okada"
    org_findings_policies = await loaders.organization_finding_policies.load(
        org_name
    )
    assert org_findings_policies == [
        OrgFindingPolicy(
            id="8b35ae2a-56a1-4f64-9da7-6a552683bf46",
            organization_name="okada",
            name="007. Cross-site request forgery",
            state=OrgFindingPolicyState(
                modified_date=datetime.fromisoformat(
                    "2021-04-26T13:37:10+00:00"
                ),
                modified_by="test2@test.com",
                status=PolicyStateStatus.APPROVED,
            ),
            tags=set(),
        ),
    ]
