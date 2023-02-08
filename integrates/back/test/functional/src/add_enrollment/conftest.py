# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enrollment.types import (
    Enrollment,
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
from db_model.trials.types import (
    Trial,
)
from db_model.types import (
    Policies,
)
import pytest
import pytest_asyncio


@pytest.mark.resolver_test_group("add_enrollment")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate() -> bool:
    data = {
        "enrollments": [
            Enrollment(
                email="janedoe@janedoe.com",
                enrolled=True,
            ),
        ],
        "trials": [
            Trial(
                email="janedoe@janedoe.com",
                completed=False,
                extension_date=None,
                extension_days=0,
                start_date=datetime.fromisoformat(
                    "2022-10-21T15:58:31.280182+00:00"
                ),
            ),
        ],
        "groups": [
            {
                "group": Group(
                    created_by="johndoe@johndoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup",
                    organization_id="e314a87c-223f-44bc-8317-75900f2ffbc7",
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
        "organizations": [
            {
                "organization": Organization(
                    created_by="johndoe@johndoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="e314a87c-223f-44bc-8317-75900f2ffbc7",
                    name="testorg",
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
        "organization_access": [
            OrganizationAccess(
                organization_id="e314a87c-223f-44bc-8317-75900f2ffbc7",
                email="johndoe@johndoe.com",
            ),
        ],
        "policies": [
            {
                "level": "organization",
                "subject": "johndoe@johndoe.com",
                "object": "testorg",
                "role": "user_manager",
            },
            {
                "level": "group",
                "subject": "johndoe@johndoe.com",
                "object": "testgroup",
                "role": "user_manager",
            },
        ],
        "stakeholders": [
            Stakeholder(
                email="johndoe@johndoe.com",
                first_name="John",
                is_registered=True,
                last_name="Doe",
            ),
            Stakeholder(
                enrolled=True,
                email="janedoe@janedoe.com",
                first_name="Jane",
                is_registered=True,
                last_name="Doe",
            ),
        ],
    }
    return await db.populate(data)
