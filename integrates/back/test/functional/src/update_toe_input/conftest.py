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


@pytest.mark.resolver_test_group("update_toe_input")
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
                        nickname="test_nickname_2",
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
        "toe_inputs": (
            ToeInput(
                component="https://test.com/test",
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
                    seen_at=None,
                    seen_first_time_by="",
                    unreliable_root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                ),
            ),
            ToeInput(
                component="192.168.1.1:8080",
                entry_point="btnTest",
                group_name="group1",
                state=ToeInputState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-02T05:00:00+00:00"
                    ),
                    attacked_by="",
                    be_present=True,
                    be_present_until=None,
                    has_vulnerabilities=False,
                    first_attack_at=datetime.fromisoformat(
                        "2021-02-02T05:00:00+00:00"
                    ),
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
                component="https://app.fluidattacks.com:8080/test",
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
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
