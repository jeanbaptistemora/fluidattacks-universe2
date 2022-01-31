from back.tests import (
    db,
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
    IPRootItem,
    IPRootMetadata,
    IPRootState,
    MachineGitRootExecution,
    URLRootItem,
    URLRootMetadata,
    URLRootState,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_toe_input")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    test_email = "admin@gmail.com"
    test_date = "2020-11-19T13:37:10+00:00"
    test_status = "ACTIVE"
    data: Dict[str, Any] = {
        "roots": (
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date=test_date,
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
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="git_1",
                    other=None,
                    reason=None,
                    status=test_status,
                    url="https://gitlab.com/fluidattacks/product",
                ),
            ),
            IPRootItem(
                group_name="group1",
                id="83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
                metadata=IPRootMetadata(type="IP"),
                state=IPRootState(
                    address="192.168.1.1",
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="ip_1",
                    other=None,
                    port="8080",
                    reason=None,
                    status=test_status,
                ),
            ),
            URLRootItem(
                group_name="group1",
                id="eee8b331-98b9-4e32-a3c7-ec22bd244ae8",
                metadata=URLRootMetadata(type="URL"),
                state=URLRootState(
                    host="app.fluidattacks.com",
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="url_1",
                    other=None,
                    path="/",
                    port="8080",
                    protocol="HTTPS",
                    reason=None,
                    status=test_status,
                ),
            ),
        ),
    }

    return await db.populate({**generic_data["db_data"], **data})
