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


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("send_trial_engagement_notification")
@pytest.fixture(autouse=True, scope="session")
async def populate() -> bool:
    data = {
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
            Company(
                domain="janedoe.com",
                trial=Trial(
                    completed=False,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-11-08T15:58:31.280182"
                    ),
                ),
            ),
            Company(
                domain="uiguaran.com",
                trial=Trial(
                    completed=False,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-11-06T15:58:31.280182"
                    ),
                ),
            ),
        ],
        "groups": [
            {
                "group": Group(
                    created_by="johndoe@johndoe.com",
                    created_date="2022-10-21T15:58:31.280182",
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup",
                    organization_id="e314a87c-223f-44bc-8317-75900f2ffbc7",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="johndoe@johndoe.com",
                        modified_date="2022-10-21T15:58:31.280182",
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.FREE,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                ),
            },
            {
                "group": Group(
                    created_by="janedoe@janedoe.com",
                    created_date="2022-10-21T15:58:31.280182",
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup2",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d25",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="janedoe@janedoe.com",
                        modified_date="2022-10-21T15:58:31.280182",
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.FREE,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                ),
            },
            {
                "group": Group(
                    created_by="uiguaran@uiguaran.com",
                    created_date="2022-10-21T15:58:31.280182",
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup3",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d26",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="uiguaran@uiguaran.com",
                        modified_date="2022-10-21T15:58:31.280182",
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
                    created_date="2022-10-21T15:58:31.280182",
                    country="Colombia",
                    id="e314a87c-223f-44bc-8317-75900f2ffbc7",
                    name="testorg",
                    policies=Policies(
                        modified_by="johndoe@johndoe.com",
                        modified_date="2022-10-21T15:58:31.280182",
                    ),
                    state=OrganizationState(
                        modified_by="johndoe@johndoe.com",
                        modified_date="2022-10-21T15:58:31.280182",
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="janedoe@janedoe.com",
                    created_date="2022-10-21T15:58:31.280182",
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d25",
                    name="testorg2",
                    policies=Policies(
                        modified_by="janedoe@janedoe.com",
                        modified_date="2022-10-21T15:58:31.280182",
                    ),
                    state=OrganizationState(
                        modified_by="janedoe@janedoe.com",
                        modified_date="2022-10-21T15:58:31.280182",
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="uiguaran@uiguaran.com",
                    created_date="2022-10-21T15:58:31.280182",
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d26",
                    name="testorg3",
                    policies=Policies(
                        modified_by="uiguaran@uiguaran.com",
                        modified_date="2022-10-21T15:58:31.280182",
                    ),
                    state=OrganizationState(
                        modified_by="uiguaran@uiguaran.com",
                        modified_date="2022-10-21T15:58:31.280182",
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
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
                email="janedoe@janedoe.com",
                first_name="Jane",
                is_registered=True,
                last_name="Doe",
            ),
            Stakeholder(
                email="uiguaran@uiguaran.com",
                first_name="Ursula",
                is_registered=True,
                last_name="Iguaran",
            ),
        ],
    }
    return await db.populate(data)
