from back.tests import (
    db,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
    OrgFindingPolicyMetadata,
    OrgFindingPolicyState,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("submit_organization_finding_policy")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    test_email = "user_manager@gmail.com"
    test_date = "2021-05-19T13:37:10+00:00"
    data: Dict[str, Any] = {
        "organization_finding_policies": (
            OrgFindingPolicyItem(
                org_name="orgtest",
                id="dd63f2df-522d-4bfa-ad85-837832c71164",
                metadata=OrgFindingPolicyMetadata(
                    name="031. Excessive privileges - AWS",
                    tags={},
                ),
                state=OrgFindingPolicyState(
                    modified_by=test_email,
                    modified_date=test_date,
                    status="REJECTED",
                ),
            ),
            OrgFindingPolicyItem(
                org_name="orgtest",
                id="3be367f9-b06c-4f72-ab77-38268045a8ff",
                metadata=OrgFindingPolicyMetadata(
                    name="037. Technical information leak",
                    tags={},
                ),
                state=OrgFindingPolicyState(
                    modified_by=test_email,
                    modified_date=test_date,
                    status="INACTIVE",
                ),
            ),
            OrgFindingPolicyItem(
                org_name="orgtest",
                id="f3f19b09-00e5-4bc7-b9ea-9999c9fe9f87",
                metadata=OrgFindingPolicyMetadata(
                    name="081. Lack of multi-factor authentication",
                    tags={},
                ),
                state=OrgFindingPolicyState(
                    modified_by=test_email,
                    modified_date=test_date,
                    status="ACTIVE",
                ),
            ),
        )
    }

    return await db.populate({**generic_data["db_data"], **data})
