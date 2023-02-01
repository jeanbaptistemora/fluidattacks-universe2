# pylint: disable=import-error
from . import (
    get_result,
)
from back.test.functional.src.organization import (
    get_result as get_organization,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    CredentialType,
)
from db_model.roots.types import (
    GitRoot,
    RootRequest,
)
import pytest
from typing import (
    cast,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_git_root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_git_root(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    credentials: dict = {
        "azureOrganization": "testorg1",
        "isPat": True,
        "token": "token",
        "name": "Credentials test",
        "type": "HTTPS",
    }

    organization: dict = await get_organization(user=email, org=org_id)
    assert (
        len(
            organization["data"]["organization"][
                "integrationRepositoriesConnection"
            ]["edges"]
        )
        == 1
    )

    result: dict = await get_result(
        user=email, group=group_name, credentials=credentials
    )
    assert "errors" not in result
    assert result["data"]["addGitRoot"]["success"]

    loaders = get_new_context()
    root_id = result["data"]["addGitRoot"]["rootId"]
    root = cast(
        GitRoot, await loaders.root.load(RootRequest(group_name, root_id))
    )
    assert root.cloning.status.value == "QUEUED"
    assert root.cloning.reason == "Cloning queued..."

    organization = await get_organization(user=email, org=org_id)
    assert (
        len(
            organization["data"]["organization"][
                "integrationRepositoriesConnection"
            ]["edges"]
        )
        == 0
    )

    org_credentials = await loaders.organization_credentials.load(org_id)
    new_credentials = next(
        (
            credential
            for credential in org_credentials
            if credential.state.name == credentials["name"]
        ),
        None,
    )

    assert new_credentials is not None
    assert new_credentials.owner == email
    assert new_credentials.state.name == credentials["name"]
    assert (
        new_credentials.state.type == CredentialType[str(credentials["type"])]
    )
    assert getattr(
        new_credentials.state.secret, "token", None
    ) == credentials.get("token")
    assert getattr(new_credentials.state, "is_pat", False) == credentials.get(
        "isPat", False
    )
    assert getattr(
        new_credentials.state, "azure_organization", None
    ) == credentials.get("azureOrganization")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_git_root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_add_git_root_fail_1(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    credentials: dict = {
        "token": "token",
        "name": "Credentials test",
        "type": "HTTPS",
    }
    result: dict = await get_result(
        user=email,
        credentials=credentials,
        group=group_name,
    )

    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Active root with the same Nickname already exists"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_git_root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
async def test_add_git_root_fail_2(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    credentials: dict = {
        "token": "token",
        "name": "Credentials test",
        "type": "HTTPS",
    }
    result: dict = await get_result(
        user=email,
        group=group_name,
        credentials=credentials,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
