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
    RootEnvironmentUrl,
)
from db_model.toe_lines.types import (
    ToeLines,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_lines_sorts")
@pytest.fixture(autouse=True, scope="session")
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
                    created_date="2020-11-19T13:37:10+00:00",
                    group_name="group1",
                    id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        environment_urls=["https://test.com"],
                        git_environment_urls=[
                            RootEnvironmentUrl(
                                url="https://test.com",
                                id="78dd64d3198473115a7f5263d27bed15f9f2fc07",
                            )
                        ],
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
                    created_date="2020-11-19T13:37:10+00:00",
                    group_name="group1",
                    id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        environment_urls=["https://test.com"],
                        git_environment_urls=[
                            RootEnvironmentUrl(
                                url="https://test.com",
                                id="78dd64d3198473115a7f5263d27bed15f9f2fc07",
                            )
                        ],
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
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
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
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                loc=180,
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
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c3",
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
