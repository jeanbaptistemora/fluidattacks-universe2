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
    URLRoot,
    URLRootState,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
    Dict,
)


@pytest.mark.resolver_test_group("update_root_cloning_status")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    test_email = "admin@gmail.com"
    test_status = RootStatus.INACTIVE
    data: dict[str, Any] = {
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-12-09T13:37:10+00:00"
                        ),
                        reason="test creation root",
                        status=GitCloningStatus("CLONING"),
                    ),
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2022-12-09T13:37:10+00:00"
                    ),
                    group_name="group2",
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
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2022-12-09T13:37:10+00:00"
                        ),
                        nickname="test_nickname_1",
                        other=None,
                        reason=None,
                        status=test_status,
                        url="https://gitlab.com/fluidattacks/repo",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": URLRoot(
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-12-09T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="4039d098-ffc5-4984-8ed3-eb17bca98e199",
                    organization_name="orgtest",
                    state=URLRootState(
                        host="test.fluidattacks.com",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2022-12-09T13:37:10+00:00"
                        ),
                        nickname="",
                        other=None,
                        path="/",
                        port="8080",
                        protocol="HTTPS",
                        reason=None,
                        status=test_status,
                    ),
                    type=RootType.URL,
                ),
                "historic_state": [],
            },
        ]
    }

    return await db.populate({**generic_data["db_data"], **data})
