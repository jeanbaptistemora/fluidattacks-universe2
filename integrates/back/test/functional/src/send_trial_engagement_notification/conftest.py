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


@pytest.mark.resolver_test_group("send_trial_engagement_notification")
@pytest_asyncio.fixture(autouse=True, scope="session")
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
            Company(
                domain="abuendia.com",
                trial=Trial(
                    completed=False,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-11-04T15:58:31.280182"
                    ),
                ),
            ),
            Company(
                domain="avicario.com",
                trial=Trial(
                    completed=False,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-11-02T15:58:31.280182"
                    ),
                ),
            ),
            Company(
                domain="fariza.com",
                trial=Trial(
                    completed=False,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-10-31T15:58:31.280182"
                    ),
                ),
            ),
            Company(
                domain="snassar.com",
                trial=Trial(
                    completed=False,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-10-29T15:58:31.280182"
                    ),
                ),
            ),
            Company(
                domain="jbuendia.com",
                trial=Trial(
                    completed=False,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-10-27T15:58:31.280182"
                    ),
                ),
            ),
            Company(
                domain="rremedios.com",
                trial=Trial(
                    completed=False,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-10-23T15:58:31.280182"
                    ),
                ),
            ),
            Company(
                domain="rmontiel.com",
                trial=Trial(
                    completed=False,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-10-22T15:58:31.280182"
                    ),
                ),
            ),
            Company(
                domain="rmoscote.com",
                trial=Trial(
                    completed=False,
                    extension_date=None,
                    extension_days=0,
                    start_date=datetime.fromisoformat(
                        "2022-10-20T15:58:31.280182"
                    ),
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
            {
                "group": Group(
                    created_by="janedoe@janedoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup2",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d25",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="janedoe@janedoe.com",
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
            {
                "group": Group(
                    created_by="uiguaran@uiguaran.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup3",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d26",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="uiguaran@uiguaran.com",
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
            {
                "group": Group(
                    created_by="abuendia@abuendia.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup4",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d27",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="abuendia@abuendia.com",
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
            {
                "group": Group(
                    created_by="avicario@avicario.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup5",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d28",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="avicario@avicario.com",
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
            {
                "group": Group(
                    created_by="fariza@fariza.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup6",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d29",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="fariza@fariza.com",
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
            {
                "group": Group(
                    created_by="snassar@snassar.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup7",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d30",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="snassar@snassar.com",
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
            {
                "group": Group(
                    created_by="jbuendia@jbuendia.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup8",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d31",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="jbuendia@jbuendia.com",
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
            {
                "group": Group(
                    created_by="rremedios@rremedios.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup9",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d32",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="rremedios@rremedios.com",
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
            {
                "group": Group(
                    created_by="rmontiel@rmontiel.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup10",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d33",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="rmontiel@rmontiel.com",
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
            {
                "group": Group(
                    created_by="rmoscote@rmoscote.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    description="test description",
                    language=GroupLanguage.EN,
                    name="testgroup11",
                    organization_id="5ee9880b-5e19-44ba-baf1-f2601bdf7d34",
                    state=GroupState(
                        has_machine=True,
                        has_squad=False,
                        managed=GroupManaged.TRIAL,
                        modified_by="rmoscote@rmoscote.com",
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
            {
                "organization": Organization(
                    created_by="janedoe@janedoe.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d25",
                    name="testorg2",
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
            {
                "organization": Organization(
                    created_by="uiguaran@uiguaran.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d26",
                    name="testorg3",
                    policies=Policies(
                        modified_by="uiguaran@uiguaran.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="uiguaran@uiguaran.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="abuendia@abuendia.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d27",
                    name="testorg4",
                    policies=Policies(
                        modified_by="abuendia@abuendia.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="abuendia@abuendia.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="avicario@avicario.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d28",
                    name="testorg5",
                    policies=Policies(
                        modified_by="avicario@avicario.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="avicario@avicario.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="fariza@fariza.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d29",
                    name="testorg6",
                    policies=Policies(
                        modified_by="fariza@fariza.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="fariza@fariza.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="snassar@snassar.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d30",
                    name="testorg7",
                    policies=Policies(
                        modified_by="snassar@snassar.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="snassar@snassar.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="jbuendia@jbuendia.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d31",
                    name="testorg8",
                    policies=Policies(
                        modified_by="jbuendia@jbuendia.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="jbuendia@jbuendia.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="rremedios@rremedios.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d32",
                    name="testorg9",
                    policies=Policies(
                        modified_by="rremedios@rremedios.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="rremedios@rremedios.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="rmontiel@rmontiel.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d33",
                    name="testorg10",
                    policies=Policies(
                        modified_by="rmontiel@rmontiel.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="rmontiel@rmontiel.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="rmoscote@rmoscote.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-21T15:58:31.280182+00:00"
                    ),
                    country="Colombia",
                    id="5ee9880b-5e19-44ba-baf1-f2601bdf7d34",
                    name="testorg11",
                    policies=Policies(
                        modified_by="rmoscote@rmoscote.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="rmoscote@rmoscote.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-21T15:58:31.280182+00:00"
                        ),
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
            Stakeholder(
                email="abuendia@abuendia.com",
                first_name="Amaranta",
                is_registered=True,
                last_name="Buendia",
            ),
            Stakeholder(
                email="avicario@avicario.com",
                first_name="Angela",
                is_registered=True,
                last_name="Vicario",
            ),
            Stakeholder(
                email="fariza@fariza.com",
                first_name="Florentino",
                is_registered=True,
                last_name="Ariza",
            ),
            Stakeholder(
                email="snassar@snassar.com",
                first_name="Santiago",
                is_registered=True,
                last_name="Nassar",
            ),
            Stakeholder(
                email="jbuendia@jbuendia.com",
                first_name="Jose",
                is_registered=True,
                last_name="Buendia",
            ),
            Stakeholder(
                email="rremedios@rremedios.com",
                first_name="Renata",
                is_registered=True,
                last_name="Remedios",
            ),
            Stakeholder(
                email="rmontiel@rmontiel.com",
                first_name="Rebeca",
                is_registered=True,
                last_name="Montiel",
            ),
            Stakeholder(
                email="rmoscote@rmoscote.com",
                first_name="Remedios",
                is_registered=True,
                last_name="Moscote",
            ),
        ],
    }
    return await db.populate(data)
