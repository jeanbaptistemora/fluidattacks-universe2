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
@pytest.mark.resolver_test_group("update_credentials")
@pytest.mark.parametrize(
    ["email", "organization_id", "credentials_id", "edited_credentials"],
    [
        [
            "user_manager@fluidattacks.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            "261bf518-f8f4-4f82-b996-3d034df44a27",
            dict(name="cred1", type="HTTPS", token="token test"),
        ],
        [
            "user@gmail.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            "9edc56a8-2743-437e-a6a9-4847b28e1fd5",
            dict(
                name="cred2", type="HTTPS", user="user user", password="99111"
            ),
        ],
        [
            "user@gmail.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            "42143c0c-a12c-4774-9d02-285b94e698e4",
            dict(
                name="cred3",
                type="SSH",
                key="LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KTUlJCg==",
            ),
        ],
    ],
)
async def test_update_credentials(
    populate: bool,
    email: str,
    organization_id: str,
    credentials_id: str,
    edited_credentials: dict[str, str],
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        organization_id=organization_id,
        credentials_id=credentials_id,
        credentials=edited_credentials,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateCredentials"]
    assert result["data"]["updateCredentials"]["success"]
    loaders: Dataloaders = get_new_context()
    org_credentials: tuple[
        Credentials, ...
    ] = await loaders.organization_credentials.load(organization_id)
    current_credentials = next(
        (
            credentials
            for credentials in org_credentials
            if credentials.id == credentials_id
        ),
        None,
    )
    assert current_credentials is not None
    assert current_credentials.owner == email
    assert current_credentials.state.name == edited_credentials["name"]
    assert (
        current_credentials.state.type
        == CredentialType[edited_credentials["type"]]
    )
    assert getattr(
        current_credentials.state.secret, "token", None
    ) == edited_credentials.get("token")
    assert getattr(
        current_credentials.state.secret, "key", None
    ) == edited_credentials.get("key")
    assert getattr(
        current_credentials.state.secret, "user", None
    ) == edited_credentials.get("user")
    assert getattr(
        current_credentials.state.secret, "password", None
    ) == edited_credentials.get("password")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_credentials")
@pytest.mark.parametrize(
    ["email", "organization_id", "credentials_id", "edited_credentials"],
    [
        [
            "user@gmail.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            "261bf518-f8f4-4f82-b996-3d034df44a27",
            dict(name="cred1", type="HTTPS", token="token test"),
        ],
        [
            "user_manager@fluidattacks.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            "42143c0c-a12c-4774-9d02-285b94e698e4",
            dict(
                name="cred3",
                type="SSH",
                key="LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KTUlJCg==",
            ),
        ],
    ],
)
async def test_update_credentials_fail(
    populate: bool,
    email: str,
    organization_id: str,
    credentials_id: str,
    edited_credentials: dict[str, str],
) -> None:
    assert populate
    result: Dict[str, Any] = await get_result(
        user=email,
        organization_id=organization_id,
        credentials_id=credentials_id,
        credentials=edited_credentials,
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Stakeholder is not the credentials owner"
    )
