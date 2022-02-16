from back.tests import (
    db,
)
from db_model.credentials.types import (
    CredentialItem,
    CredentialMetadata,
    CredentialState,
)
from db_model.enums import (
    CredentialType,
    GitCloningStatus,
)
from db_model.roots.types import (
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_git_root")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data = {
        "credentials": (
            CredentialItem(
                group_name="group1",
                id="3912827d-2b35-4e08-bd35-1bb24457951d",
                metadata=CredentialMetadata(type=CredentialType.SSH),
                state=CredentialState(
                    key="VGVzdCBTU0gK",
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-10T14:58:10+00:00",
                    name="SSH Key",
                    roots=["88637616-41d4-4242-854a-db8ff7fe1ab6"],
                ),
            ),
            CredentialItem(
                group_name="group1",
                id="1a5dacda-1d52-465c-9158-f6fd5dfe0998",
                metadata=CredentialMetadata(type=CredentialType.SSH),
                state=CredentialState(
                    key="VGVzdCBTU0gK",
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-10T14:58:10+00:00",
                    name="SSH Key",
                    roots=["9059f0cb-3b55-404b-8fc5-627171f424ad"],
                ),
            ),
        ),
        "roots": (
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2022-02-10T14:58:10+00:00",
                    reason="Cloned successfully",
                    status=GitCloningStatus.OK,
                ),
                group_name="group1",
                id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                metadata=GitRootMetadata(type="Git"),
                organization_name="orgtest",
                state=GitRootState(
                    branch="master",
                    environment_urls=[],
                    environment="production",
                    git_environment_urls=[],
                    gitignore=[],
                    includes_health_check=False,
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-10T14:58:10+00:00",
                    nickname="nickname",
                    other="",
                    reason="",
                    status="ACTIVE",
                    url="https://gitlab.com/fluidattacks/nickname",
                ),
            ),
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2022-02-10T14:58:10+00:00",
                    reason="Cloned successfully",
                    status=GitCloningStatus.OK,
                ),
                group_name="group1",
                id="9059f0cb-3b55-404b-8fc5-627171f424ad",
                metadata=GitRootMetadata(type="Git"),
                organization_name="orgtest",
                state=GitRootState(
                    branch="master",
                    environment_urls=[],
                    environment="production",
                    git_environment_urls=[],
                    gitignore=[],
                    includes_health_check=False,
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-10T14:58:10+00:00",
                    nickname="nickname2",
                    other="",
                    reason="",
                    status="ACTIVE",
                    url="https://gitlab.com/fluidattacks/nickname2",
                ),
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
