# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.types import (
    Policies,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("grant_stakeholder_organization_access")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "organizations": [
            {
                "organization": Organization(
                    created_by=generic_data["global_vars"]["user_email"],
                    created_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    country="Colombia",
                    id="40f6da5f-4f66-4bf0-825b-a2d9748ad6dc",
                    name="orgtest2",
                    policies=Policies(
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
