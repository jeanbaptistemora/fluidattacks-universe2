from custom_exceptions import (
    FindingNamePolicyNotFound,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
    OrgFindingPolicyMetadata,
    OrgFindingPolicyState,
)
from organizations_finding_policies import (
    domain as policies_domain,
)
import pytest

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_by_group() -> None:
    org_name = "okada"
    finding_policy_id = "8b35ae2a-56a1-4f64-9da7-6a552683bf46"
    assert await policies_domain.get_finding_policy(
        org_name=org_name,
        finding_policy_id=finding_policy_id,
    ) == OrgFindingPolicyItem(
        id="8b35ae2a-56a1-4f64-9da7-6a552683bf46",
        org_name="okada",
        metadata=OrgFindingPolicyMetadata(
            name="007. Cross-site request forgery",
            tags={},
        ),
        state=OrgFindingPolicyState(
            modified_date="2021-04-26T13:37:10+00:00",
            modified_by="test2@test.com",
            status="APPROVED",
        ),
    )
    with pytest.raises(FindingNamePolicyNotFound):
        assert await policies_domain.get_finding_policy(
            org_name=org_name,
            finding_policy_id="5d92c7eb-816f-43d5-9361-c0672837e7ab",
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
                tags={},
            ),
            state=OrgFindingPolicyState(
                modified_date="2021-04-26T13:37:10+00:00",
                modified_by="test2@test.com",
                status="APPROVED",
            ),
        ),
    )
