from back.tests import (
    db,
)
from collections import (
    defaultdict,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_organization_access")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    new_user: str = "justoneorgacess@test.com"
    organization_id: str = "ed3831e8-14a2-483b-9cff-cc0747829640"
    data: Dict[str, Any] = {
        "orgs": [
            {
                "name": "orgtest5",
                "id": organization_id,
                "users": [
                    generic_data["global_vars"][
                        "customer_manager_fluid_email"
                    ],
                    new_user,
                    generic_data["global_vars"]["admin_email"],
                ],
                "groups": [
                    "group5",
                ],
                "policy": {},
                "max_acceptance_days": 7,
            },
        ],
        "users": [
            {
                "email": new_user,
                "first_login": "",
                "first_name": "new_user",
                "last_login": "",
                "last_name": "new_user",
                "legal_remember": False,
                "push_tokens": [],
                "is_registered": True,
            },
        ],
        "groups": [
            {
                "project_name": "group5",
                "description": "group5 description",
                "language": "en",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_drills": True,
                        "has_forces": True,
                        "requester": "unknown",
                        "service": "WHITE",
                        "type": "continuous",
                    }
                ],
                "project_status": "ACTIVE",
            },
        ],
        "policies": [
            {
                "level": "organization",
                "subject": generic_data["global_vars"][
                    "customer_manager_fluid_email"
                ],
                "object": organization_id,
                "role": "customer_manager",
            },
            {
                "level": "organization",
                "subject": new_user,
                "object": organization_id,
                "role": "user",
            },
            {
                "level": "organization",
                "subject": generic_data["global_vars"]["admin_email"],
                "object": organization_id,
                "role": "admin",
            },
            {
                "level": "group",
                "subject": generic_data["global_vars"][
                    "customer_manager_fluid_email"
                ],
                "object": "group5",
                "role": "customer_manager",
            },
            {
                "level": "group",
                "subject": new_user,
                "object": "group5",
                "role": "user",
            },
            {
                "level": "group",
                "subject": generic_data["global_vars"]["admin_email"],
                "object": "group5",
                "role": "admin",
            },
        ],
    }
    merge_dict = defaultdict(list)
    for dict_data in (generic_data["db_data"], data):
        for key, value in dict_data.items():
            merge_dict[key].extend(value)

    return await db.populate(merge_dict)
