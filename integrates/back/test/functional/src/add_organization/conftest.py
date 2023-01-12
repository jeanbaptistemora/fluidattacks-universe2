# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.companies.types import (
    Company,
    Trial,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.types import (
    Policies,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
    Dict,
)


@pytest.mark.resolver_test_group("add_organization")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "companies": [
            Company(
                domain="johndoe.com",
                trial=Trial(
                    completed=False,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-10-25T15:58:31.280182"
                    ),
                ),
            ),
        ],
        "groups": [],
        "organizations": [
            {
                "organization": Organization(
                    created_by="johndoe@johndoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="967e17db-6345-4504-a5c4-285e5f8068c6",
                    name="trialorg",
                    policies=Policies(
                        modified_by="johndoe@johndoe.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="johndoe@johndoe.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ],
        "policies": [
            *generic_data["db_data"]["policies"],
            {
                "level": "organization",
                "subject": "johndoe@johndoe.com",
                "object": "ORG#967e17db-6345-4504-a5c4-285e5f8068c6",
                "role": "user_manager",
            },
        ],
        "stakeholders": [
            *generic_data["db_data"]["stakeholders"],
            Stakeholder(
                email="johndoe@johndoe.com",
                first_name="John",
                is_registered=True,
                last_name="Doe",
                role="user_manager",
            ),
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
