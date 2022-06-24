from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.credentials.types import (
    Credential,
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
            "admin@gmail.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            dict(name="cred1", type="HTTPS", token="token test"),
        ],
        [
            "user@gmail.com",
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
                key="LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KTUlJRW9K",
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
        Credential, ...
    ] = await loaders.organization_credentials_new.load(organization_id)
    new_credentials = next(
        (
            credential
            for credential in org_credentials
            if credential.state.name == credentials["name"]
        ),
        None,
    )
    assert new_credentials is not None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_credentials")
@pytest.mark.parametrize(
    ["email", "organization_id", "credentials"],
    [
        [
            "admin@gmail.com",
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
