# flake8: noqa
from back.test import (
    db,
)
from db_model.enums import (
    GitCloningStatus,
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
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("move_root")
@pytest.fixture(autouse=True, scope="session")
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
        "orgs": (
            {
                "name": "wano",
                "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                "users": ("test@fluidattacks.com",),
                "groups": (
                    "kibi",
                    "kuri",
                    "udon",
                ),
                "policy": {},
            },
            {
                "name": "zou",
                "id": "5da92d2e-cb16-4d0f-bb10-bbe2186886e4",
                "users": ("test@fluidattacks.com",),
                "groups": ("kurau",),
                "policy": {},
            },
        ),
        "groups": (
            {
                "group": Group(
                    description="-",
                    language=GroupLanguage.EN,
                    name="kibi",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        modified_by="test@fluidattacks.com",
                        modified_date="2020-05-20T22:00:00+00:00",
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
                    description="-",
                    language=GroupLanguage.EN,
                    name="kuri",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        modified_by="test@fluidattacks.com",
                        modified_date="2020-05-20T22:00:00+00:00",
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
                    description="-",
                    language=GroupLanguage.EN,
                    name="udon",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        modified_by="test@fluidattacks.com",
                        modified_date="2020-05-20T22:00:00+00:00",
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
                    description="-",
                    language=GroupLanguage.EN,
                    name="kurau",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        modified_by="test@fluidattacks.com",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="5da92d2e-cb16-4d0f-bb10-bbe2186886e4",
                ),
            },
        ),
        "roots": (
            GitRoot(
                cloning=GitRootCloning(
                    modified_date="2022-02-10T14:58:10+00:00",
                    reason="Cloned successfully",
                    status=GitCloningStatus.OK,
                ),
                group_name="kibi",
                id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                organization_name="wano",
                state=GitRootState(
                    branch="master",
                    environment_urls=[],
                    environment="production",
                    git_environment_urls=[],
                    gitignore=[],
                    includes_health_check=False,
                    modified_by="test@fluidattacks.com",
                    modified_date="2022-02-10T14:58:10+00:00",
                    nickname="test",
                    other="",
                    reason="",
                    status=RootStatus.ACTIVE,
                    url="https://gitlab.com/fluidattacks/test",
                ),
                type=RootType.GIT,
            ),
            GitRoot(
                cloning=GitRootCloning(
                    modified_date="2022-02-10T14:58:10+00:00",
                    reason="Cloned successfully",
                    status=GitCloningStatus.OK,
                ),
                group_name="kibi",
                id="8a62109b-316a-4a88-a1f1-767b80383864",
                organization_name="wano",
                state=GitRootState(
                    branch="master",
                    environment_urls=[],
                    environment="production",
                    git_environment_urls=[],
                    gitignore=[],
                    includes_health_check=False,
                    modified_by="test@fluidattacks.com",
                    modified_date="2022-02-10T14:58:10+00:00",
                    nickname="inactive",
                    other="",
                    reason="",
                    status=RootStatus.INACTIVE,
                    url="https://gitlab.com/fluidattacks/inactive",
                ),
                type=RootType.GIT,
            ),
        ),
    }
    return await db.populate(data)
