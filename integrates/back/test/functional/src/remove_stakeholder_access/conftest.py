# pylint: disable=import-error
from back.test import (
    db,
)
from collections import (
    defaultdict,
)
from datetime import (
    datetime,
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
from db_model.organization_access.types import (
    OrganizationAccess,
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
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_stakeholder_access")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    new_user: str = "justonegroupaccess@gmail.com"
    organization_id = "e75525d6-70a6-45ba-9f87-66c2dd2678d9"
    data: dict[str, Any] = {
        "organizations": [
            {
                "organization": Organization(
                    created_by=generic_data["global_vars"][
                        "customer_manager_fluid_email"
                    ],
                    created_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    country="Colombia",
                    id="e75525d6-70a6-45ba-9f87-66c2dd2678d9",
                    name="orgtest4",
                    policies=Policies(
                        modified_by=generic_data["global_vars"][
                            "customer_manager_fluid_email"
                        ],
                        max_acceptance_days=7,
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by=generic_data["global_vars"][
                            "customer_manager_fluid_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ],
        "organization_access": [
            OrganizationAccess(
                organization_id=organization_id,
                email=generic_data["global_vars"][
                    "customer_manager_fluid_email"
                ],
            ),
            OrganizationAccess(
                organization_id=organization_id,
                email=new_user,
            ),
            OrganizationAccess(
                organization_id=organization_id,
                email=generic_data["global_vars"]["admin_email"],
            ),
        ],
        "stakeholders": [
            Stakeholder(
                email=new_user,
                first_name="new_user",
                last_name="new_user",
                legal_remember=False,
                is_registered=True,
            ),
        ],
        "groups": [
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="group4 description",
                    language=GroupLanguage.EN,
                    name="group4",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
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
