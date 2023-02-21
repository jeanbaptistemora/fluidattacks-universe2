# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingState,
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
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderPhone,
)
from db_model.types import (
    Policies,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityUnreliableIndicators,
)
import pytest
import pytest_asyncio


@pytest.mark.resolver_test_group("move_root")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate() -> bool:
    data = {
        "policies": (
            {
                "level": "user",
                "subject": "test@fluidattacks.com",
                "object": "self",
                "role": "admin",
            },
        ),
        "stakeholders": [
            Stakeholder(
                email="test@fluidattacks.com",
                first_name="",
                last_name="",
                phone=StakeholderPhone(
                    calling_country_code="1",
                    country_code="US",
                    national_number="1111111111",
                ),
                legal_remember=False,
                is_registered=True,
            ),
        ],
        "organizations": (
            {
                "organization": Organization(
                    created_by="test@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    country="Colombia",
                    id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    name="wano",
                    policies=Policies(
                        modified_by="test@fluidattacks.com",
                        max_acceptance_days=7,
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by="test@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    country="Colombia",
                    id="5da92d2e-cb16-4d0f-bb10-bbe2186886e4",
                    name="zou",
                    policies=Policies(
                        modified_by="test@fluidattacks.com",
                        max_acceptance_days=7,
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ),
        "organization_access": [
            OrganizationAccess(
                organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                email="test@fluidattacks.com",
            ),
            OrganizationAccess(
                organization_id="5da92d2e-cb16-4d0f-bb10-bbe2186886e4",
                email="test@fluidattacks.com",
            ),
        ],
        "groups": (
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="-",
                    language=GroupLanguage.EN,
                    name="kibi",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
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
                    name="kuri",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
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
                    name="udon",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.BLACK,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
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
                    name="kurau",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="5da92d2e-cb16-4d0f-bb10-bbe2186886e4",
                ),
            },
        ),
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="kibi",
                    id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    organization_name="wano",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="test",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/test",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="kibi",
                    id="8a62109b-316a-4a88-a1f1-767b80383864",
                    organization_name="wano",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="inactive",
                        other="",
                        reason="",
                        status=RootStatus.INACTIVE,
                        url="https://gitlab.com/fluidattacks/inactive",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
        ],
        "findings": (
            {
                "finding": Finding(
                    id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
                    group_name="kibi",
                    state=FindingState(
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection",
                    hacker_email="test@fluidattacks.com",
                ),
                "historic_state": [],
                "historic_verification": [],
            },
        ),
        "vulnerabilities": (
            {
                "vulnerability": Vulnerability(
                    created_by="test@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:11+00:00"
                    ),
                    finding_id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
                    group_name="kibi",
                    hacker_email="test@fluidattacks.com",
                    id="64bf8e56-0b3c-432a-bff7-c3eef56c47b7",
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    state=VulnerabilityState(
                        modified_by="test@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.20",
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                    ),
                ),
            },
        ),
    }
    return await db.populate(data)
