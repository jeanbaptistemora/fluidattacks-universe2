from back.tests import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
    MachineGitRootExecution,
)
from db_model.services_toe_lines.types import (
    ServicesToeLines,
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
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "roots": (
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2020-11-19T13:37:10+00:00",
                    reason="root creation",
                    status=GitCloningStatus("UNKNOWN"),
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
                    status=GitCloningStatus("UNKNOWN"),
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
        "services_toe_lines": (
            ServicesToeLines(
                comments="comment test",
                filename="test/test#.config",
                group_name="group1",
                loc=8,
                modified_commit="983466z",
                modified_date="2019-08-01T05:00:00+00:00",
                root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                tested_date="2021-02-28T05:00:00+00:00",
                tested_lines=4,
                sorts_risk_level=0,
            ),
            ServicesToeLines(
                comments="comment test",
                filename="test2/test.sh",
                group_name="group1",
                loc=120,
                modified_commit="273412t",
                modified_date="2020-11-19T05:00:00+00:00",
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                tested_date="2021-01-20T05:00:00+00:00",
                tested_lines=172,
                sorts_risk_level=0,
            ),
            ServicesToeLines(
                comments="comment test",
                filename="test3/test.config",
                group_name="group1",
                loc=55,
                modified_commit="g545435i",
                modified_date="2020-11-19T05:00:00+00:00",
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                tested_date="2021-01-20T05:00:00+00:00",
                tested_lines=33,
                sorts_risk_level=0,
            ),
        ),
        "toe_lines": (
            ToeLines(
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
                filename="test/test#.config",
                first_attack_at=datetime.fromisoformat(
                    "2020-01-19T15:41:04+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                last_author="customer1@gmail.com",
                last_commit="273412t",
                loc=4324,
                modified_date=datetime.fromisoformat(
                    "2020-11-16T15:41:04+00:00"
                ),
                root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                seen_at=datetime.fromisoformat("2020-01-01T15:41:04+00:00"),
                sorts_risk_level=0,
            ),
            ToeLines(
                attacked_at=datetime.fromisoformat(
                    "2021-02-20T05:00:00+00:00"
                ),
                attacked_by="test2@test.com",
                attacked_lines=4,
                be_present=True,
                be_present_until=None,
                comments="comment 2",
                filename="test2/test.sh",
                first_attack_at=datetime.fromisoformat(
                    "2020-02-19T15:41:04+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                last_author="customer2@gmail.com",
                last_commit="983466z",
                loc=8,
                modified_date=datetime.fromisoformat(
                    "2020-11-15T15:41:04+00:00"
                ),
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                seen_at=datetime.fromisoformat("2020-02-01T15:41:04+00:00"),
                sorts_risk_level=0,
            ),
            ToeLines(
                attacked_at=datetime.fromisoformat(
                    "2021-01-20T05:00:00+00:00"
                ),
                attacked_by="test3@test.com",
                attacked_lines=120,
                be_present=True,
                be_present_until=None,
                comments="comment 3",
                filename="test3/test.config",
                first_attack_at=datetime.fromisoformat(
                    "2020-01-14T15:41:04+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                last_author="customer3@gmail.com",
                last_commit="g545435i",
                loc=243,
                modified_date=datetime.fromisoformat(
                    "2020-11-16T15:41:04+00:00"
                ),
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                seen_at=datetime.fromisoformat("2019-01-01T15:41:04+00:00"),
                sorts_risk_level=0,
            ),
        ),
    }

    return await db.populate({**generic_data["db_data"], **data})
