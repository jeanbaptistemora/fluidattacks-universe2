# pylint: disable=import-error
from back.test.unit.src.utils import (
    get_mock_response,
    get_mocked_path,
)
from custom_exceptions import (
    CredentialAlreadyExists,
)
from dataloaders import (
    get_new_context,
)
from db_model.credentials.types import (
    OauthGitlabSecret,
)
import json
from organizations.validations import (
    validate_credentials_oauth,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["organization_id", "user_email"],
    [
        [
            "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
            "unittest@fluidattacks.com",
        ],
    ],
)
@patch(
    get_mocked_path("loaders.organization_credentials.load"),
    new_callable=AsyncMock,
)
async def test_validate_credentials_oauth(
    mock_organization_credentials_loader: AsyncMock,
    organization_id: str,
    user_email: str,
) -> None:
    mock_organization_credentials_loader.return_value = get_mock_response(
        get_mocked_path("loaders.organization_credentials.load"),
        json.dumps(["1a5dacda-1d52-465c-9158-f6fd5dfe0998"]),
    )
    await validate_credentials_oauth(
        loaders=get_new_context(),
        organization_id=organization_id,
        user_email=user_email,
        secret_type=OauthGitlabSecret,
    )
    with pytest.raises(CredentialAlreadyExists):
        await validate_credentials_oauth(
            loaders=get_new_context(),
            organization_id=organization_id,
            user_email="admin@gmail.com",
            secret_type=OauthGitlabSecret,
        )
