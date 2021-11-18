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
from db_model.toe_lines.types import (
    ToeLines,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_lines")
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
                    nickname="product",
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
                    nickname="asm_1",
                    other=None,
                    reason=None,
                    status="INACTIVE",
                    url="https://gitlab.com/fluidattacks/asm_1",
                ),
            ),
        ),
        "toe_lines": (
            ToeLines(
                attacked_at="2021-01-20T05:00:00+00:00",
                attacked_by="test@test.com",
                attacked_lines=23,
                be_present=False,
                be_present_until="2021-01-19T15:41:04+00:00",
                comments="comment 1",
                commit_author="customer1@gmail.com",
                filename="test1/test.sh",
                first_attack_at="2020-01-19T15:41:04+00:00",
                group_name="group1",
                loc=4324,
                modified_commit="273412t",
                modified_date="2020-11-16T15:41:04+00:00",
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                seen_at="2020-01-01T15:41:04+00:00",
                sorts_risk_level=0,
            ),
            ToeLines(
                attacked_at="2021-02-20T05:00:00+00:00",
                attacked_by="test2@test.com",
                attacked_lines=4,
                be_present=True,
                be_present_until="",
                comments="comment 2",
                commit_author="customer2@gmail.com",
                filename="test2/test#.config",
                first_attack_at="2020-02-19T15:41:04+00:00",
                group_name="group1",
                loc=8,
                modified_commit="983466z",
                modified_date="2020-11-15T15:41:04+00:00",
                root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                seen_at="2020-02-01T15:41:04+00:00",
                sorts_risk_level=80,
            ),
            ToeLines(
                attacked_at="2021-01-20T05:00:00+00:00",
                attacked_by="test3@test.com",
                attacked_lines=120,
                be_present=True,
                be_present_until="",
                comments="comment 3",
                commit_author="customer3@gmail.com",
                filename="test3/test.sh",
                first_attack_at="2020-01-14T15:41:04+00:00",
                group_name="group1",
                loc=243,
                modified_commit="g545435i",
                modified_date="2020-11-16T15:41:04+00:00",
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                seen_at="2019-01-01T15:41:04+00:00",
                sorts_risk_level=-1,
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
