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
from db_model.enums import (
    GitCloningStatus,
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
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
)
from db_model.toe_lines.types import (
    ToeLines,
    ToeLinesState,
)
import pytest
import pytest_asyncio


@pytest.mark.resolver_test_group("update_toe_lines_sorts")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict) -> bool:
    data: dict = {
        "groups": [
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="This is a dummy description",
                    language=GroupLanguage.EN,
                    name="group1",
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
                    business_id="123",
                    business_name="acme",
                    sprint_duration=3,
                ),
            },
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="This is another dummy description",
                    language=GroupLanguage.EN,
                    name="group2",
                    state=GroupState(
                        has_machine=False,
                        has_squad=False,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.BLACK,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.ONESHOT,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                ),
            },
        ],
        "policies": [
            {
                "level": "group",
                "subject": "user_manager@gmail.com",
                "object": "group2",
                "role": "user_manager",
            },
        ],
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="universe",
                        other=None,
                        reason=None,
                        status=RootStatus.INACTIVE,
                        url="https://gitlab.com/fluidattacks/universe",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=["node_modules/*"],
                        includes_health_check=True,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="asm_1",
                        other=None,
                        reason=None,
                        status=RootStatus.INACTIVE,
                        url="https://gitlab.com/fluidattacks/asm_1",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
        ],
        "toe_lines": (
            ToeLines(
                filename="test/test#.config",
                group_name="group1",
                root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2021-01-20T05:00:00+00:00"
                    ),
                    attacked_by="test@test.com",
                    attacked_lines=23,
                    be_present=False,
                    be_present_until=datetime.fromisoformat(
                        "2021-01-19T15:41:04+00:00"
                    ),
                    comments="comment 1",
                    first_attack_at=datetime.fromisoformat(
                        "2020-01-19T15:41:04+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer1@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    loc=4324,
                    modified_by="test@test.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-01-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=0,
                ),
            ),
        ),
    }

    merge_dict = defaultdict(list)
    for dict_data in (generic_data["db_data"], data):
        for key, value in dict_data.items():
            if key == "groups":
                merge_dict[key] = value
            else:
                merge_dict[key].extend(value)

    return await db.populate(merge_dict)
