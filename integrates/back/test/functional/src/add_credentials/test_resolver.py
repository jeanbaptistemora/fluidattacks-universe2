from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.enums import (
    CredentialType,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_credentials")
@pytest.mark.parametrize(
    ["email", "organization_id", "credentials"],
    [
        [
            "admin@fluidattacks.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            dict(name="cred1", type="HTTPS", token="token test"),
        ],
        [
            "user@fluidattacks.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            dict(
                name="cred2", type="HTTPS", user="user test", password="test"
            ),
        ],
        [
            "user_manager@fluidattacks.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            dict(
                name="cred3",
                type="SSH",
                key="LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KTUlJCg==",
            ),
        ],
    ],
)
async def test_add_credentials(
    populate: bool,
    email: str,
    organization_id: str,
    credentials: dict[str, str],
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email, organization_id=organization_id, credentials=credentials
    )
    assert "errors" not in result
    assert "success" in result["data"]["addCredentials"]
    assert result["data"]["addCredentials"]["success"]
    loaders: Dataloaders = get_new_context()
    org_credentials: tuple[
        Credentials, ...
    ] = await loaders.organization_credentials.load(organization_id)
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
    assert new_credentials.state.type == CredentialType[credentials["type"]]
    assert getattr(
        new_credentials.state.secret, "token", None
    ) == credentials.get("token")
    assert getattr(
        new_credentials.state.secret, "key", None
    ) == credentials.get("key")
    assert getattr(
        new_credentials.state.secret, "user", None
    ) == credentials.get("user")
    assert getattr(
        new_credentials.state.secret, "password", None
    ) == credentials.get("password")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_credentials")
@pytest.mark.parametrize(
    ["email", "organization_id", "credentials"],
    [
        [
            "admin@fluidattacks.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            dict(name="cred4", type="SSH", key="YWJ"),
        ],
    ],
)
async def test_add_credentials_fail(
    populate: bool,
    email: str,
    organization_id: str,
    credentials: dict[str, str],
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email, organization_id=organization_id, credentials=credentials
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The ssh key must be in base64"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_credentials")
@pytest.mark.parametrize(
    ["email", "organization_id", "credentials"],
    [
        [
            "user@gmail.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            dict(name="cred4", type="SSH", key="YWJ"),
        ],
    ],
)
async def test_add_credentials_fail_2(
    populate: bool,
    email: str,
    organization_id: str,
    credentials: dict[str, str],
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email, organization_id=organization_id, credentials=credentials
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
