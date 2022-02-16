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
    GitRootState,
    IPRootItem,
    IPRootState,
    URLRootItem,
    URLRootState,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("activate_root")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    test_email = "admin@gmail.com"
    test_date = "2020-11-19T13:37:10+00:00"
    test_status = "INACTIVE"
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
                organization_name="orgtest",
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
                    nickname="",
                    other=None,
                    reason=None,
                    status=test_status,
                    url="https://gitlab.com/fluidattacks/product",
                ),
                type="Git",
            ),
            IPRootItem(
                group_name="group2",
                id="83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
                organization_name="orgtest",
                state=IPRootState(
                    address="192.168.1.1",
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="",
                    other=None,
                    port="8080",
                    reason=None,
                    status=test_status,
                ),
                type="IP",
            ),
            URLRootItem(
                group_name="group2",
                id="eee8b331-98b9-4e32-a3c7-ec22bd244ae8",
                organization_name="orgtest",
                state=URLRootState(
                    host="app.fluidattacks.com",
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="",
                    other=None,
                    path="/",
                    port="8080",
                    protocol="HTTPS",
                    reason=None,
                    status=test_status,
                ),
                type="URL",
            ),
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date=test_date,
                    reason="root creation",
                    status=GitCloningStatus("UNKNOWN"),
                ),
                group_name="group2",
                id="702b81b3-d741-4699-9173-ecbc30bfb0cb",
                organization_name="orgtest",
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
                    nickname="",
                    other=None,
                    reason=None,
                    status=test_status,
                    url="https://gitlab.com/fluidattacks/repo",
                ),
                type="Git",
            ),
            IPRootItem(
                group_name="group1",
                id="44db9bee-c97d-4161-98c6-f124d7dc9a41",
                organization_name="orgtest",
                state=IPRootState(
                    # FP: local testing
                    address="192.168.1.2",  # NOSONAR
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="",
                    other=None,
                    port="8080",
                    reason=None,
                    status=test_status,
                ),
                type="IP",
            ),
            URLRootItem(
                group_name="group1",
                id="bd4e5e66-da26-4274-87ed-17de7c3bc2f1",
                organization_name="orgtest",
                state=URLRootState(
                    host="test.fluidattacks.com",
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="",
                    other=None,
                    path="/",
                    port="8080",
                    protocol="HTTPS",
                    reason=None,
                    status=test_status,
                ),
                type="URL",
            ),
        )
    }

    return await db.populate({**generic_data["db_data"], **data})
