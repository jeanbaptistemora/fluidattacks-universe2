from back.tests import (
    db,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
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
                    nickname="",
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
                    nickname="",
                    other=None,
                    reason=None,
                    status="INACTIVE",
                    url="https://gitlab.com/fluidattacks/asm_1",
                ),
            ),
        ),
        "toe_lines": (
            ToeLines(
                comments="comment test",
                filename="product/test/test#.config",
                group_name="group1",
                loc=8,
                modified_commit="983466z",
                modified_date="2019-08-01T00:00:00-05:00",
                root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                tested_date="2021-02-28T00:00:00-05:00",
                tested_lines=4,
                sorts_risk_level=0,
            ),
            ToeLines(
                comments="comment test",
                filename="asm_1/test2/test.sh",
                group_name="group1",
                loc=172,
                modified_commit="273412t",
                modified_date="2020-11-19T00:00:00-05:00",
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                tested_date="2021-01-20T00:00:00-05:00",
                tested_lines=120,
                sorts_risk_level=0,
            ),
            ToeLines(
                comments="comment test",
                filename="asm_1/test3/test.config",
                group_name="group1",
                loc=55,
                modified_commit="g545435i",
                modified_date="2020-11-19T00:00:00-05:00",
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                tested_date="2021-01-20T00:00:00-05:00",
                tested_lines=33,
                sorts_risk_level=0,
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
