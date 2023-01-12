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
)


@pytest.mark.resolver_test_group("add_group")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "companies": [
            Company(
                domain="gmail.com",
                trial=Trial(
                    completed=True,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-10-25T15:58:31.280182"
                    ),
                ),
            ),
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
            Company(
                domain="janedoe.com",
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
        "organizations": [
            {
                "organization": Organization(
                    created_by=generic_data["global_vars"]["user_email"],
                    created_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    country="Colombia",
                    id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    name="orgtest",
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
            {
                "organization": Organization(
                    created_by="johndoe@johndoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="54b37c94-ebd4-416d-97b3-dee412fc2a1d",
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
            {
                "organization": Organization(
                    created_by="janedoe@janedoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="56f222da-c912-4441-a015-36ec2aad58fc",
                    name="trialorg2",
                    policies=Policies(
                        modified_by="janedoe@janedoe.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="janedoe@janedoe.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ],
        "groups": [
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="-",
                    language=GroupLanguage.EN,
                    name="group2",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.BLACK,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.ONESHOT,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    sprint_start_date=datetime.fromisoformat(
                        "2022-06-06T00:00:00+00:00"
                    ),
                ),
            },
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="-",
                    language=GroupLanguage.EN,
                    name="group3",
                    state=GroupState(
                        has_machine=False,
                        has_squad=False,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.BLACK,
                        status=GroupStateStatus.DELETED,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.ONESHOT,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    sprint_start_date=datetime.fromisoformat(
                        "2022-06-06T00:00:00+00:00"
                    ),
                ),
            },
            {
                "group": Group(
                    created_by="johndoe@johndoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="-",
                    language=GroupLanguage.EN,
                    name="trialgroup1",
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="johndoe@johndoe.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.FREE,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                ),
            },
        ],
        "policies": [
            *generic_data["db_data"]["policies"],
            {
                "level": "organization",
                "subject": "johndoe@johndoe.com",
                "object": "ORG#54b37c94-ebd4-416d-97b3-dee412fc2a1d",
                "role": "user_manager",
            },
            {
                "level": "organization",
                "subject": "janedoe@janedoe.com",
                "object": "ORG#56f222da-c912-4441-a015-36ec2aad58fc",
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
            Stakeholder(
                email="janedoe@janedoe.com",
                first_name="Jane",
                is_registered=True,
                last_name="Doe",
                role="user_manager",
            ),
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
