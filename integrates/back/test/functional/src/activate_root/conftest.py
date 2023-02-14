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
    IPRoot,
    IPRootState,
    RootEnvironmentUrl,
    URLRoot,
    URLRootState,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("activate_root")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    test_email = "admin@gmail.com"
    test_status = RootStatus.INACTIVE
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
                    created_by=test_email,
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
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="",
                        other=None,
                        reason=None,
                        status=test_status,
                        url="https://gitlab.com/fluidattacks/universe",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
                "git_environment_urls": [
                    RootEnvironmentUrl(
                        url="https://test.com",
                        id="78dd64d3198473115a7f5263d27bed15f9f2fc07",
                    )
                ],
            },
            {
                "root": IPRoot(
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group2",
                    id="83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.1",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="",
                        other=None,
                        reason=None,
                        status=test_status,
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
                    group_name="group2",
                    id="eee8b331-98b9-4e32-a3c7-ec22bd244ae8",
                    organization_name="orgtest",
                    state=URLRootState(
                        host="app.fluidattacks.com",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
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
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group2",
                    id="702b81b3-d741-4699-9173-ecbc30bfb0cb",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        environment_urls=["https://test.com"],
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="",
                        other=None,
                        reason=None,
                        status=test_status,
                        url="https://gitlab.com/fluidattacks/repo",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
                "git_environment_urls": [
                    RootEnvironmentUrl(
                        url="https://test.com",
                        id="78dd64d3198473115a7f5263d27bed15f9f2fc07",
                    )
                ],
            },
            {
                "root": IPRoot(
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="44db9bee-c97d-4161-98c6-f124d7dc9a41",
                    organization_name="orgtest",
                    state=IPRootState(
                        # FP: local testing
                        address="192.168.1.2",  # NOSONAR
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="",
                        other=None,
                        reason=None,
                        status=test_status,
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
                    id="bd4e5e66-da26-4274-87ed-17de7c3bc2f1",
                    organization_name="orgtest",
                    state=URLRootState(
                        host="test.fluidattacks.com",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
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
