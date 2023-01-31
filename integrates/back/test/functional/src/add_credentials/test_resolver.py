from . import (
    get_result,
)
from custom_exceptions import (
    InvalidCredentialSecret,
    InvalidParameter,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    CredentialType,
)
import pytest
from typing import (
    Any,
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
                name="cred2",
                type="HTTPS",
                user="user test",
                password="lorem.ipsum,Dolor.sit:am3t;t]{3[s.T}/l;u=r<w>oiu(p",
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
        [
            "user_manager@fluidattacks.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            dict(
                name="cred4",
                type="HTTPS",
                azureOrganization="orgcred5",
                isPat=True,
                token="token test",
            ),
        ],
    ],
)
async def test_add_credentials(
    populate: bool,
    email: str,
    organization_id: str,
    credentials: dict,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email, organization_id=organization_id, credentials=credentials
    )
    assert "errors" not in result
    assert "success" in result["data"]["addCredentials"]
    assert result["data"]["addCredentials"]["success"]
    loaders = get_new_context()
    org_credentials = await loaders.organization_credentials.load(
        organization_id
    )
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
    assert getattr(new_credentials.state, "is_pat", False) == credentials.get(
        "isPat", False
    )
    assert getattr(
        new_credentials.state, "azure_organization", None
    ) == credentials.get("azureOrganization")


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
    result: dict[str, Any] = await get_result(
        user=email, organization_id=organization_id, credentials=credentials
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - The ssh key must be in base64"
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(name=" ", type="SSH", key="YWJ"),
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Field cannot fill with blank characters"
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(name="cred5", type="HTTPS", token=" "),
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Field cannot fill with blank characters"
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            name="cred5", type="HTTPS", token="token test", isPat=True
        ),
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(
        InvalidParameter("azure_organization")
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            name="cred5",
            type="HTTPS",
            token="token test",
            isPat=False,
            azureOrganization="testorg1",
        ),
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(
        InvalidParameter("azure_organization")
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            name="cred5",
            type="HTTPS",
            token="token test",
            isPat=True,
            azureOrganization="   ",
        ),
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Field cannot fill with blank characters"
    )
    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            name="cred6",
            type="SSH",
            key="LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KTUlJCg==",
            isPat=True,
            azureOrganization="testorgcred6",
        ),
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(InvalidCredentialSecret())
    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            name="cred6",
            type="HTTPS",
            user="user test",
            password="lorem.ipsum,Dolor.sit:am3t;t]{3[s.T}/l;u=r<w>oiu(p",
            isPat=True,
            azureOrganization="testorgcred6",
        ),
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(InvalidCredentialSecret())

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            # FP: local testing
            name="cred5",
            type="HTTPS",
            user=" ",
            password="124",  # NOSONAR
        ),
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Field cannot fill with blank characters"
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            # FP: local testing
            name="cred5",
            type="HTTPS",
            user="usertest",
            password="124",  # NOSONAR
        ),
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Password should start with a letter"
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            # FP: local testing
            name="cred5",
            type="HTTPS",
            user="usertest",
            password="ttr",  # NOSONAR
        ),
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Password should include at least one number"
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            # FP: local testing
            name="cred5",
            type="HTTPS",
            user="usertest",
            password="TT1L",  # NOSONAR
        ),
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Password should include lowercase characters"
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            # FP: local testing
            name="cred5",
            type="HTTPS",
            user="usertest",
            password="tt1l",  # NOSONAR
        ),
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Password should include uppercase characters"
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            # FP: local testing
            name="cred5",
            type="HTTPS",
            user="usertest",
            password="ttbcd3Tl",  # NOSONAR
        ),
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Password should not include sequentials characters"
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            # FP: local testing
            name="cred6",
            type="HTTPS",
            user="usertest",
            password="ttbd3Tl",  # NOSONAR
        ),
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Invalid field length in form"
    )

    result = await get_result(
        user=email,
        organization_id=organization_id,
        credentials=dict(
            # FP: local testing
            name="cred7",
            type="HTTPS",
            user="usertest",
            password="loremripsumlDolornsitlam3txconsectetrttbd3Tl",  # NOSONAR
        ),
    )
    assert "errors" in result
    assert (
        result["errors"][0]["message"]
        == "Exception - Password should include symbols characters"
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
    result: dict[str, Any] = await get_result(
        user=email, organization_id=organization_id, credentials=credentials
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
