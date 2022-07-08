# pylint: disable=import-error
from back.test import (
    db,
)
from collections import (
    defaultdict,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
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
        "organizations": [
            {
                "organization": Organization(
                    id=organization_id,
                    name="orgtest5",
                    policies=Policies(
                        modified_by=generic_data["global_vars"][
                            "customer_manager_fluid_email"
                        ],
                        modified_date="2019-11-22T20:07:57+00:00",
                    ),
                    state=OrganizationState(
                        modified_by=generic_data["global_vars"][
                            "customer_manager_fluid_email"
                        ],
                        modified_date="2019-11-22T20:07:57+00:00",
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ],
        "organization_users": [
            {
                "id": organization_id,
                "users": [
                    generic_data["global_vars"][
                        "customer_manager_fluid_email"
                    ],
                    new_user,
                    generic_data["global_vars"]["admin_email"],
                ],
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
                "registered": True,
            },
        ],
        "groups": [
            {
                "group": Group(
                    description="group5 description",
                    language=GroupLanguage.EN,
                    name="group5",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANUALLY"],
                        modified_by="unknown",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                ),
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
