from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.types import (
    GitRoot,
)
from organizations.utils import (
    get_organization,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_credentials")
@pytest.mark.parametrize(
    ["email", "organization_id", "credentials_id"],
    [
        [
            "user@fluidattacks.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            "9edc56a8-2743-437e-a6a9-4847b28e1fd5",
        ],
    ],
)
async def test_remove_credentials(
    populate: bool,
    email: str,
    organization_id: str,
    credentials_id: str,
) -> None:
    assert populate
    loaders = get_new_context()
    org_credentials = await loaders.organization_credentials.load(
        organization_id
    )
    new_credentials = next(
        (
            credentials
            for credentials in org_credentials
            if credentials.id == credentials_id
        ),
        None,
    )
    assert new_credentials is not None
    result: dict[str, Any] = await get_result(
        user=email,
        organization_id=organization_id,
        credentials_id=credentials_id,
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeCredentials"]
    assert result["data"]["removeCredentials"]["success"]
    loaders = get_new_context()
    org_credentials = await loaders.organization_credentials.load(
        organization_id
    )
    new_credentials = next(
        (
            credentials
            for credentials in org_credentials
            if credentials.id == credentials_id
        ),
        None,
    )
    assert new_credentials is None
    organization = await get_organization(loaders, organization_id)
    organization_git_roots = tuple(
        root
        for root in await loaders.organization_roots.load(organization.name)
        if isinstance(root, GitRoot)
    )
    for root in organization_git_roots:
        assert root.state.credential_id != credentials_id


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_credentials")
@pytest.mark.parametrize(
    ["email", "organization_id", "credentials_id"],
    [
        [
            "user@gmail.com",
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            "261bf518-f8f4-4f82-b996-3d034df44a27",
        ],
    ],
)
async def test_remove_credentials_fails(
    populate: bool,
    email: str,
    organization_id: str,
    credentials_id: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        organization_id=organization_id,
        credentials_id=credentials_id,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
