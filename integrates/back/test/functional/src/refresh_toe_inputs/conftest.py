# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    URLRoot,
    URLRootState,
)
from db_model.toe_inputs.types import (
    ToeInput,
    ToeInputState,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("refresh_toe_inputs")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
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
                        "2022-02-10T14:58:10+00:00"
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
                        nickname="test_nickname_1",
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
                "root": URLRoot(
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                    organization_name="orgtest",
                    state=URLRootState(
                        host="app.fluidattacks.com",
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="test_nickname_2",
                        other=None,
                        path="/",
                        port="8080",
                        protocol="HTTPS",
                        reason=None,
                        status=RootStatus.INACTIVE,
                    ),
                    type=RootType.URL,
                ),
                "historic_state": [],
            },
            {
                "root": URLRoot(
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
                    organization_name="orgtest",
                    state=URLRootState(
                        host="app.fluidattacks.com",
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="test_nickname_3",
                        other=None,
                        path="/",
                        port="8080",
                        protocol="HTTPS",
                        reason=None,
                        status=RootStatus.ACTIVE,
                    ),
                    type=RootType.URL,
                ),
                "historic_state": [],
            },
        ],
        "toe_inputs": (
            ToeInput(
                component="test.com/api/Test",
                entry_point="idTest",
                group_name="group1",
                state=ToeInputState(
                    attacked_at=datetime.fromisoformat(
                        "2020-01-02T05:00:00+00:00"
                    ),
                    attacked_by="",
                    be_present=True,
                    be_present_until=None,
                    first_attack_at=datetime.fromisoformat(
                        "2020-01-02T05:00:00+00:00"
                    ),
                    has_vulnerabilities=False,
                    modified_by="hacker@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-02T06:00:00+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2000-01-01T05:00:00+00:00"
                    ),
                    seen_first_time_by="",
                    unreliable_root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                ),
            ),
            ToeInput(
                component="test.com/test/test.aspx",
                entry_point="btnTest",
                group_name="group1",
                state=ToeInputState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-02T05:00:00+00:00"
                    ),
                    attacked_by="",
                    be_present=True,
                    be_present_until=None,
                    first_attack_at=datetime.fromisoformat(
                        "2021-02-02T05:00:00+00:00"
                    ),
                    has_vulnerabilities=False,
                    modified_by="hacker@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-02T06:00:00+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-03-14T05:00:00+00:00"
                    ),
                    seen_first_time_by="test@test.com",
                    unreliable_root_id="",
                ),
            ),
            ToeInput(
                component="test.com/test2/test.aspx",
                entry_point="-",
                group_name="group1",
                state=ToeInputState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    attacked_by="",
                    be_present=False,
                    be_present_until=datetime.fromisoformat(
                        "2021-03-11T05:00:00+00:00"
                    ),
                    first_attack_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    has_vulnerabilities=False,
                    modified_by="hacker@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-02T06:00:00+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-01-11T05:00:00+00:00"
                    ),
                    seen_first_time_by="test2@test.com",
                    unreliable_root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                ),
            ),
            ToeInput(
                component="test.com/test3/test.aspx",
                entry_point="-",
                group_name="group1",
                state=ToeInputState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    attacked_by="",
                    be_present=False,
                    be_present_until=datetime.fromisoformat(
                        "2021-03-11T05:00:00+00:00"
                    ),
                    first_attack_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    has_vulnerabilities=False,
                    modified_by="hacker@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-02T06:00:00+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-01-11T05:00:00+00:00"
                    ),
                    seen_first_time_by="test3@test.com",
                    unreliable_root_id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
                ),
            ),
            ToeInput(
                component="test.com/test4/test.aspx",
                entry_point="-",
                group_name="group1",
                state=ToeInputState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    attacked_by="",
                    be_present=False,
                    be_present_until=datetime.fromisoformat(
                        "2021-03-11T05:00:00+00:00"
                    ),
                    first_attack_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    has_vulnerabilities=False,
                    modified_by="hacker@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-02T06:00:00+00:00"
                    ),
                    seen_at=None,
                    seen_first_time_by="test4@test.com",
                    unreliable_root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                ),
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
