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
    StakeholderAccessToken,
)
from db_model.types import (
    Policies,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("remove_stakeholder_organization_access")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    new_user: str = "justoneorgaccess@test.com"
    organization_id: str = "ed3831e8-14a2-483b-9cff-cc0747829640"
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
                    id=organization_id,
                    name="orgtest5",
                    policies=Policies(
                        modified_by=generic_data["global_vars"][
                            "customer_manager_fluid_email"
                        ],
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
                access_token=StakeholderAccessToken(
                    iat=1634677195,
                    jti="c8d9d5f058cf200f7435508fc2dba37d07447ec12dcd07",
                    salt="27c7f38dd7cc432871c84b63e78cd716739c40055253c",
                ),
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
                    description="group5 description",
                    language=GroupLanguage.EN,
                    name="group5",
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
