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
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    IPRoot,
    IPRootState,
    RootEnvironmentUrl,
    URLRoot,
    URLRootState,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_input")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    test_email = "admin@gmail.com"
    test_status = "ACTIVE"
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
                        environment_urls=["https://test.com"],
                        git_environment_urls=[
                            RootEnvironmentUrl(
                                url="https://test.com",
                                id="78dd64d3198473115a7f5263d27bed15f9f2fc07",
                                group_name="group_1",
                            )
                        ],
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="git_1",
                        other=None,
                        reason=None,
                        status=test_status,  # type: ignore
                        url="https://gitlab.com/fluidattacks/universe",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": IPRoot(
                    created_by=test_email,
                    created_date="2020-11-19T13:37:10+00:00",
                    group_name="group1",
                    id="83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.1",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="ip_1",
                        other=None,
                        reason=None,
                        status=test_status,  # type: ignore
                    ),
                    type=RootType.IP,
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
                    id="eee8b331-98b9-4e32-a3c7-ec22bd244ae8",
                    organization_name="orgtest",
                    state=URLRootState(
                        host="app.fluidattacks.com",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="url_1",
                        other=None,
                        path="/",
                        port="8080",
                        protocol="HTTPS",
                        reason=None,
                        status=test_status,  # type: ignore
                    ),
                    type=RootType.URL,
                ),
                "historic_state": [],
            },
        ],
    }

    return await db.populate({**generic_data["db_data"], **data})
