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
    Policies,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_access")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    new_user: str = "justonegroupacess@gmail.com"
    data: dict[str, Any] = {
        "organizations": [
            {
                "organization": Organization(
                    id="e75525d6-70a6-45ba-9f87-66c2dd2678d9",
                    name="orgtest4",
                    policies=Policies(
                        modified_by=generic_data["global_vars"][
                            "customer_manager_fluid_email"
                        ],
                        max_acceptance_days=7,
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
                "id": "e75525d6-70a6-45ba-9f87-66c2dd2678d9",
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
                    description="group4 description",
                    language=GroupLanguage.EN,
                    name="group4",
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
                    organization_id="e75525d6-70a6-45ba-9f87-66c2dd2678d9",
                ),
            },
        ],
        "policies": [
            {
                "level": "group",
                "subject": generic_data["global_vars"][
                    "customer_manager_fluid_email"
                ],
                "object": "group4",
                "role": "customer_manager",
            },
            {
                "level": "organization",
                "subject": generic_data["global_vars"][
                    "customer_manager_fluid_email"
                ],
                "object": "e75525d6-70a6-45ba-9f87-66c2dd2678d9",
                "role": "customer_manager",
            },
            {
                "level": "group",
                "subject": new_user,
                "object": "group4",
                "role": "user",
            },
            {
                "level": "organization",
                "subject": new_user,
                "object": "e75525d6-70a6-45ba-9f87-66c2dd2678d9",
                "role": "user",
            },
            {
                "level": "group",
                "subject": generic_data["global_vars"]["admin_email"],
                "object": "group4",
                "role": "admin",
            },
            {
                "level": "organization",
                "subject": generic_data["global_vars"]["admin_email"],
                "object": "e75525d6-70a6-45ba-9f87-66c2dd2678d9",
                "role": "admin",
            },
        ],
    }
    merge_dict = defaultdict(list)
    for dict_data in (generic_data["db_data"], data):
        for key, value in dict_data.items():
            merge_dict[key].extend(value)

    return await db.populate(merge_dict)
