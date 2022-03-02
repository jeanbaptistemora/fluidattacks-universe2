from back.tests import (
    db,
)
from batch.enums import (
    Action,
)
from datetime import (
    datetime,
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
    GitRootState,
)
from newutils.datetime import (
    get_as_epoch,
    get_now,
)
import pytest
from typing import (
    Any,
    Dict,
    Tuple,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data = {
        "groups": [
            {
                "project_name": "group1",
                "description": "this is group1",
                "language": "en",
                "group_context": "This is a dummy context",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_squad": True,
                        "has_forces": True,
                        "has_machine": True,
                        "requester": "unknown",
                        "service": "WHITE",
                        "type": "continuous",
                    }
                ],
                "project_status": "ACTIVE",
            },
            {
                "project_name": "group2",
                "description": "this is group2",
                "language": "en",
                "group_context": "This is a dummy context",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_squad": True,
                        "has_forces": True,
                        "has_machine": True,
                        "requester": "unknown",
                        "service": "WHITE",
                        "type": "continuous",
                    }
                ],
                "project_status": "ACTIVE",
            },
        ],
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
            CredentialItem(
                group_name="group1",
                id="4a5dacda-1d52-365c-5158-f6fd5dfe0999",
                metadata=CredentialMetadata(type=CredentialType.SSH),
                state=CredentialState(
                    key="VGVzdCBTU0gK",
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-10T14:58:10+00:00",
                    name="SSH Key",
                    roots=["2159f8cb-3b55-404b-8fc5-627171f424ax"],
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
                    nickname="nickname1",
                    other="",
                    reason="",
                    status="ACTIVE",
                    url="https://gitlab.com/fluidattacks/nickname",
                ),
                type="Git",
            ),
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2022-02-10T14:58:10+00:00",
                    reason="Failed to clone",
                    status=GitCloningStatus.FAILED,
                ),
                group_name="group1",
                id="2159f8cb-3b55-404b-8fc5-627171f424ax",
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
                type="Git",
            ),
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2022-02-10T14:58:10+00:00",
                    reason="Cloned successfully",
                    status=GitCloningStatus.FAILED,
                ),
                group_name="group1",
                id="88637616-41d4-4242-854a-db8ff7fe1ab6",
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
                    nickname="nicknam3",
                    other="",
                    reason="",
                    status="ACTIVE",
                    url="https://gitlab.com/fluidattacks/nickname",
                ),
                type="Git",
            ),
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2022-02-10T14:58:10+00:00",
                    reason="Cloned successfully",
                    status=GitCloningStatus.OK,
                ),
                group_name="group1",
                id="5059f0cb-4b55-404b-3fc5-627171f424af",
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
                    nickname="nickname4",
                    other="",
                    reason="",
                    status="ACTIVE",
                    url="https://gitlab.com/fluidattacks/nickname2",
                ),
                type="Git",
            ),
        ),
    }
    actions: Tuple[Dict[str, Any]] = (
        dict(
            action_name=Action.CLONE_ROOTS,
            entity="group1",
            subject=generic_data["global_vars"]["admin_email"],
            time=str(get_as_epoch(get_now())),
            additional_info="nickname1,nickname2,nickname3,nickname4",
            batch_job_id=None,
            queue="spot_soon",
            key="1",
        ),
        dict(
            action_name=Action.CLONE_ROOTS,
            entity="group1",
            subject=generic_data["global_vars"]["admin_email"],
            time=str(get_as_epoch(get_now())),
            additional_info="nickname1,nickname3",
            batch_job_id=None,
            queue="spot_soon",
            key="2",
        ),
        dict(
            action_name=Action.CLONE_ROOTS,
            entity="group1",
            subject=generic_data["global_vars"]["admin_email"],
            time=str(get_as_epoch(get_now())),
            additional_info="nickname6",
            batch_job_id=None,
            queue="spot_soon",
            key="3",
        ),
    )
    await db.populate_actions(actions)
    return await db.populate({**generic_data["db_data"], **data})
