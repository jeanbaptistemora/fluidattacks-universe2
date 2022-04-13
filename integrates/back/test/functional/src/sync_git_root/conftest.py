# pylint: disable=import-error
from back.test import (
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
    GitRootState,
)
import os
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("sync_git_root")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data = {
        "actions": (
            {
                "action_name": "clone_roots",
                "additional_info": "nickname5",
                "entity": "group1",
                "subject": "admin@gmail.com",
                "time": "1644596859",
            },
            {
                "action_name": "clone_roots",
                "additional_info": "nickname5",
                "entity": "group1",
                "subject": "admin@gmail.com",
                "time": "1644596852",
            },
        ),
        "credentials": (
            CredentialItem(
                group_name="group1",
                id="261bf518-f8f4-4f82-b996-3d034df44a27",
                metadata=CredentialMetadata(CredentialType.SSH),
                state=CredentialState(
                    key=os.environ["TEST_SSH_KEY"],
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-11 11:32:15+00:00",
                    name="Good SSH Key",
                    roots=["e22a3a0d-05ac-4d13-8c81-7c829f8f96e3"],
                ),
            ),
            CredentialItem(
                group_name="group1",
                id="9edc56a8-2743-437e-a6a9-4847b28e1fd5",
                metadata=CredentialMetadata(CredentialType.SSH),
                state=CredentialState(
                    key="VGVzdCBTU0ggS2V5Cg==",
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-11 11:32:15+00:00",
                    name="Bad SSH Key",
                    roots=[
                        "888648ed-a71c-42e5-b3e5-c3a370d26c68",
                        "c75f9c2c-1984-49cf-bd3f-c628175a569c",
                    ],
                ),
            ),
        ),
        "roots": (
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2022-02-11 11:32:15+00:00",
                    reason="Repo added",
                    status=GitCloningStatus.UNKNOWN,
                ),
                group_name="group1",
                id="e22a3a0d-05ac-4d13-8c81-7c829f8f96e3",
                organization_name="orgtest",
                state=GitRootState(
                    branch="master",
                    environment_urls=[],
                    environment="production",
                    git_environment_urls=[],
                    gitignore=[],
                    includes_health_check=False,
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-11 11:32:15+00:00",
                    nickname="nickname1",
                    other=None,
                    reason=None,
                    status="ACTIVE",
                    url="git@gitlab.com:fluidattacks/product.git",
                ),
                type="Git",
            ),
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2022-02-11 11:32:15+00:00",
                    reason="Repo added",
                    status=GitCloningStatus.UNKNOWN,
                ),
                group_name="group1",
                id="888648ed-a71c-42e5-b3e5-c3a370d26c68",
                organization_name="orgtest",
                state=GitRootState(
                    branch="master",
                    environment_urls=[],
                    environment="production",
                    git_environment_urls=[],
                    gitignore=[],
                    includes_health_check=False,
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-11 11:32:15+00:00",
                    nickname="nickname2",
                    other=None,
                    reason=None,
                    status="ACTIVE",
                    url="git@gitlab.com:fluidattacks/product.git",
                ),
                type="Git",
            ),
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2022-02-11 11:32:15+00:00",
                    reason="Repo added",
                    status=GitCloningStatus.UNKNOWN,
                ),
                group_name="group1",
                id="3626aca5-099c-42b9-aa25-d8c6e0aab98f",
                organization_name="orgtest",
                state=GitRootState(
                    branch="master",
                    environment_urls=[],
                    environment="production",
                    git_environment_urls=[],
                    gitignore=[],
                    includes_health_check=False,
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-11 11:32:15+00:00",
                    nickname="nickname3",
                    other=None,
                    reason=None,
                    status="ACTIVE",
                    url="git@gitlab.com:fluidattacks/product.git",
                ),
                type="Git",
            ),
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2022-02-11 11:32:15+00:00",
                    reason="Repo added",
                    status=GitCloningStatus.UNKNOWN,
                ),
                group_name="group1",
                id="58167a02-08c2-4cdf-a5e4-568398cbe7cb",
                organization_name="orgtest",
                state=GitRootState(
                    branch="master",
                    environment_urls=[],
                    environment="production",
                    git_environment_urls=[],
                    gitignore=[],
                    includes_health_check=False,
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-11 11:32:15+00:00",
                    nickname="nickname4",
                    other=None,
                    reason=None,
                    status="INACTIVE",
                    url="git@gitlab.com:fluidattacks/product.git",
                ),
                type="Git",
            ),
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2022-02-11 11:32:15+00:00",
                    reason="Repo added",
                    status=GitCloningStatus.UNKNOWN,
                ),
                group_name="group1",
                id="c75f9c2c-1984-49cf-bd3f-c628175a569c",
                organization_name="orgtest",
                state=GitRootState(
                    branch="master",
                    environment_urls=[],
                    environment="production",
                    git_environment_urls=[],
                    gitignore=[],
                    includes_health_check=False,
                    modified_by="admin@gmail.com",
                    modified_date="2022-02-11 11:32:15+00:00",
                    nickname="nickname5",
                    other=None,
                    reason=None,
                    status="ACTIVE",
                    url="git@gitlab.com:fluidattacks/product.git",
                ),
                type="Git",
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
