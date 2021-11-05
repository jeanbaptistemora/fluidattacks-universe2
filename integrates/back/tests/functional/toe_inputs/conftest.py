from back.tests import (
    db,
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
                commit="hh66uu5",
                component="test.com/api/Test",
                created_date="2000-01-01T05:00:00+00:00",
                entry_point="idTest",
                group_name="group1",
                seen_first_time_by="",
                tested_date="2020-01-02T00:00:00-05:00",
                verified="Yes",
                unreliable_root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                vulns="FIN.S.0001.Test",
            ),
            ToeInput(
                commit="e91320h",
                component="test.com/test/test.aspx",
                created_date="2020-03-14T00:00:00-05:00",
                entry_point="btnTest",
                group_name="group1",
                seen_first_time_by="test@test.com",
                tested_date="2021-02-02T00:00:00-05:00",
                unreliable_root_id="",
                verified="No",
                vulns="",
            ),
            ToeInput(
                commit="d83027t",
                component="test.com/test2/test.aspx",
                created_date="2020-01-11T00:00:00-05:00",
                entry_point="-",
                group_name="group1",
                seen_first_time_by="test2@test.com",
                tested_date="2021-02-11T00:00:00-05:00",
                unreliable_root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                verified="No",
                vulns="FIN.S.0003.Test",
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
