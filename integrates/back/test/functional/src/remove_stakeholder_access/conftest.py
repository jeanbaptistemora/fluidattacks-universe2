# pylint: disable=import-error
from back.test import (
    db,
)
from collections import (
    defaultdict,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_access")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    new_user: str = "justonegroupacess@gmail.com"
    data: Dict[str, Any] = {
        "orgs": [
            {
                "name": "orgtest4",
                "id": "e75525d6-70a6-45ba-9f87-66c2dd2678d9",
                "users": [
                    generic_data["global_vars"][
                        "customer_manager_fluid_email"
                    ],
                    new_user,
                    generic_data["global_vars"]["admin_email"],
                ],
                "groups": [
                    "group4",
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
                        managed=True,
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
