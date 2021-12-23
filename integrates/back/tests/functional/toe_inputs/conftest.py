from back.tests import (
    db,
)
from datetime import (
    datetime,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
    MachineGitRootExecution,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_inputs")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "roots": (
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2020-11-19T13:37:10+00:00",
                    reason="root creation",
                    status="UNKNOWN",
                ),
                group_name="group1",
                id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                machine_execution=MachineGitRootExecution(
                    queue_date="2021-10-08T16:58:12.499243",
                    finding_code="F122",
                    job_id="78c546bh-dgf5-47e4-a7b3-4a1ebbsd0623",
                ),
                metadata=GitRootMetadata(type="Git"),
                state=GitRootState(
                    branch="master",
                    environment="production",
                    environment_urls=["https://test.com"],
                    git_environment_urls=[
                        GitEnvironmentUrl(url="https://test.com")
                    ],
                    gitignore=["bower_components/*", "node_modules/*"],
                    includes_health_check=True,
                    modified_by="admin@gmail.com",
                    modified_date="2020-11-19T13:37:10+00:00",
                    nickname="test_nickname_1",
                    other=None,
                    reason=None,
                    status="INACTIVE",
                    url="https://gitlab.com/fluidattacks/product",
                ),
            ),
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2020-11-19T13:37:10+00:00",
                    reason="root creation",
                    status="UNKNOWN",
                ),
                group_name="group1",
                id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                machine_execution=MachineGitRootExecution(
                    queue_date="2021-10-08T16:58:12.499243",
                    finding_code="F122",
                    job_id="78c546bh-dgf5-47e4-a7b3-4a1ebbsd0623",
                ),
                metadata=GitRootMetadata(type="Git"),
                state=GitRootState(
                    branch="master",
                    environment="production",
                    environment_urls=["https://test.com"],
                    git_environment_urls=[
                        GitEnvironmentUrl(url="https://test.com")
                    ],
                    gitignore=["node_modules/*"],
                    includes_health_check=True,
                    modified_by="admin@gmail.com",
                    modified_date="2020-11-19T13:37:10+00:00",
                    nickname="test_nickname_2",
                    other=None,
                    reason=None,
                    status="INACTIVE",
                    url="https://gitlab.com/fluidattacks/asm_1",
                ),
            ),
        ),
        "toe_inputs": (
            ToeInput(
                attacked_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                attacked_by="",
                be_present=True,
                be_present_until=None,
                component="test.com/api/Test",
                entry_point="idTest",
                first_attack_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                group_name="group1",
                seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
                seen_first_time_by="",
                unreliable_root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
            ),
            ToeInput(
                attacked_at=datetime.fromisoformat(
                    "2021-02-02T05:00:00+00:00"
                ),
                attacked_by="",
                be_present=True,
                be_present_until=None,
                component="test.com/test/test.aspx",
                entry_point="btnTest",
                first_attack_at=datetime.fromisoformat(
                    "2021-02-02T05:00:00+00:00"
                ),
                group_name="group1",
                seen_at=datetime.fromisoformat("2020-03-14T05:00:00+00:00"),
                seen_first_time_by="test@test.com",
                unreliable_root_id="",
            ),
            ToeInput(
                attacked_at=datetime.fromisoformat(
                    "2021-02-11T05:00:00+00:00"
                ),
                attacked_by="",
                be_present=False,
                be_present_until=datetime.fromisoformat(
                    "2021-03-11T05:00:00+00:00"
                ),
                component="test.com/test2/test.aspx",
                entry_point="-",
                first_attack_at=datetime.fromisoformat(
                    "2021-02-11T05:00:00+00:00"
                ),
                group_name="group1",
                seen_at=datetime.fromisoformat("2020-01-11T05:00:00+00:00"),
                seen_first_time_by="test2@test.com",
                unreliable_root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
