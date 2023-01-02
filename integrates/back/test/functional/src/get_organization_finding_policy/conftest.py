# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.organization_finding_policies.enums import (
    PolicyStateStatus,
)
from db_model.organization_finding_policies.types import (
    OrgFindingPolicy,
    OrgFindingPolicyState,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("get_organization_finding_policy")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    test_email = "vulnerability_manager@gmail.com"
    test_date = datetime.fromisoformat("2023-01-02T13:37:10+00:00")
    data: dict[str, Any] = {
        "organization_finding_policies": (
            OrgFindingPolicy(
                organization_name="orgtest",
                id="dd63f2df-522d-4bfa-ad85-837832c71164",
                name="037. Technical information leak",
                tags=set(),
                state=OrgFindingPolicyState(
                    modified_by=test_email,
                    modified_date=test_date,
                    status=PolicyStateStatus.INACTIVE,
                ),
            ),
            OrgFindingPolicy(
                organization_name="orgtest",
                id="3be367f9-b06c-4f72-ab77-38268045a8ff",
                name="009. Sensitive information in source code",
                tags=set(),
                state=OrgFindingPolicyState(
                    modified_by=test_email,
                    modified_date=test_date,
                    status=PolicyStateStatus.APPROVED,
                ),
            ),
            OrgFindingPolicy(
                organization_name="orgtest",
                id="f3f19b09-00e5-4bc7-b9ea-9999c9fe9f87",
                name="371. DOM-Based cross-site scripting (XSS)",
                tags=set(),
                state=OrgFindingPolicyState(
                    modified_by=test_email,
                    modified_date=test_date,
                    status=PolicyStateStatus.SUBMITTED,
                ),
            ),
        )
    }

    return await db.populate({**generic_data["db_data"], **data})
