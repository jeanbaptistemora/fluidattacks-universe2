from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
)
from newutils.datetime import (
    get_now_minus_delta,
)
from oauth.azure import (
    get_azure_token,
)
from oauth.bitbucket import (
    get_bitbucket_token,
)
from oauth.gitlab import (
    get_token,
)
import pytest
from unittest.mock import (
    AsyncMock,
    MagicMock,
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["credential"],
    [
        [
            Credentials(
                id="1a5dacda-1d52-465c-9158-f6fd5dfe0998",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-12T14:58:10+00:00"
                    ),
                    name="oauth lab token",
                    type=CredentialType.OAUTH,
                    secret=OauthGitlabSecret(
                        refresh_token="UFUzdCBTU0gK",
                        redirect_uri="",
                        access_token="TETzdCBTU0gK",
                        valid_until=get_now_minus_delta(hours=2),
                    ),
                    is_pat=False,
                ),
            ),
        ],
    ],
)
@patch(
    "oauth.gitlab.update_credential_state",
    new_callable=AsyncMock,
)
@patch(
    "aiohttp.client.ClientSession.post",
    new_callable=MagicMock,
)
async def test_get_token(
    mock_credentials_update_credential_state: AsyncMock,
    mock_client_post: MagicMock,
    credential: Credentials,
) -> None:
    loaders = get_new_context()
    mock_client_post.return_value.__aenter__.return_value.status = 200
    mock_client_post.return_value.__aenter__.return_value.json.return_value = {
        "refresh_token": "refresh atoken",
        "access_token": "access atoken",
        "created_at": datetime.now().timestamp(),
        "expires_in": 7200,
    }

    assert await get_token(credential=credential, loaders=loaders) is not None

    assert mock_credentials_update_credential_state.called is True


@pytest.mark.parametrize(
    ["credential"],
    [
        [
            Credentials(
                id="185bbb03-8aee-4634-88c5-d1dfa0b20e10",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-12T14:58:10+00:00"
                    ),
                    name="oauth hub token",
                    type=CredentialType.OAUTH,
                    secret=OauthGithubSecret(
                        access_token="TGTzdCBTU0gK",
                    ),
                    is_pat=False,
                ),
            ),
        ],
    ],
)
@patch(
    "oauth.gitlab.update_credential_state",
    new_callable=AsyncMock,
)
async def test_get_token_fail(
    mock_credentials_update_credential_state: AsyncMock,
    credential: Credentials,
) -> None:
    loaders = get_new_context()
    assert await get_token(credential=credential, loaders=loaders) is None

    assert mock_credentials_update_credential_state.called is False


@pytest.mark.parametrize(
    ["credential"],
    [
        [
            Credentials(
                id="5990e0ec-dc8f-4c9a-82cc-9da9fbb35c11",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-17T14:58:10+00:00"
                    ),
                    name="oauth ure token",
                    type=CredentialType.OAUTH,
                    secret=OauthAzureSecret(
                        arefresh_token="CFCzdCBTU0gK",
                        redirect_uri="",
                        access_token="DEDzdCBTU0gK",
                        valid_until=get_now_minus_delta(hours=1),
                    ),
                    is_pat=False,
                ),
            ),
        ],
    ],
)
@patch(
    "oauth.azure.update_credential_state",
    new_callable=AsyncMock,
)
@patch(
    "aiohttp.client.ClientSession.post",
    new_callable=MagicMock,
)
async def test_azure_get_token(
    mock_credentials_update_credential_state: AsyncMock,
    mock_client_post: MagicMock,
    credential: Credentials,
) -> None:
    loaders = get_new_context()
    mock_client_post.return_value.__aenter__.return_value.status = 200
    mock_client_post.return_value.__aenter__.return_value.json.return_value = {
        "refresh_token": "refresh ztoken",
        "access_token": "access ztoken",
        "expires_in": 3600,
    }

    assert (
        await get_azure_token(credential=credential, loaders=loaders)
        is not None
    )

    assert mock_credentials_update_credential_state.called is True


@pytest.mark.parametrize(
    ["credential"],
    [
        [
            Credentials(
                id="3912827d-2b35-4e08-bd35-1bb24457951d",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    name="SSH Key",
                    type=CredentialType.SSH,
                    secret=SshSecret(key="VGVzdCBTU0gK"),
                    is_pat=False,
                ),
            ),
        ],
    ],
)
@patch(
    "oauth.azure.update_credential_state",
    new_callable=AsyncMock,
)
async def test_get_azure_token_fail(
    mock_credentials_update_credential_state: AsyncMock,
    credential: Credentials,
) -> None:
    loaders = get_new_context()
    assert (
        await get_azure_token(credential=credential, loaders=loaders) is None
    )

    assert mock_credentials_update_credential_state.called is False


@pytest.mark.parametrize(
    ["credential"],
    [
        [
            Credentials(
                id="1531f854-76f3-480e-8ba2-324d925096e2",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-07-17T14:58:10+00:00"
                    ),
                    name="oauth ket token",
                    type=CredentialType.OAUTH,
                    secret=OauthBitbucketSecret(
                        brefresh_token="LFLzdCBTU0gK",
                        access_token="PEPzdCBTU0gK",
                        valid_until=get_now_minus_delta(hours=1),
                    ),
                    is_pat=False,
                ),
            ),
        ],
    ],
)
@patch(
    "oauth.bitbucket.update_credential_state",
    new_callable=AsyncMock,
)
@patch(
    "aiohttp.client.ClientSession.post",
    new_callable=MagicMock,
)
async def test_get_bitbucket_token(
    mock_credentials_update_credential_state: AsyncMock,
    mock_client_post: MagicMock,
    credential: Credentials,
) -> None:
    loaders = get_new_context()
    mock_client_post.return_value.__aenter__.return_value.status = 200
    mock_client_post.return_value.__aenter__.return_value.json.return_value = {
        "refresh_token": "refresh btoken",
        "access_token": "access btoken",
        "expires_in": 7200,
    }

    assert (
        await get_bitbucket_token(credential=credential, loaders=loaders)
        is not None
    )

    assert mock_credentials_update_credential_state.called is True


@pytest.mark.parametrize(
    ["credential"],
    [
        [
            Credentials(
                id="6312a600-c131-452d-83e8-bcc4e4b33c12",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-12-17T14:58:10+00:00"
                    ),
                    name="oauth ure token",
                    type=CredentialType.OAUTH,
                    secret=OauthAzureSecret(
                        arefresh_token="OFOzdCBTU0gK",
                        redirect_uri="",
                        access_token="RERzdCBTU0gK",
                        valid_until=get_now_minus_delta(hours=1),
                    ),
                    is_pat=False,
                ),
            ),
        ],
    ],
)
@patch(
    "oauth.azure.update_credential_state",
    new_callable=AsyncMock,
)
async def test_get_bitbucket_token_fail(
    mock_credentials_update_credential_state: AsyncMock,
    credential: Credentials,
) -> None:
    loaders = get_new_context()
    assert (
        await get_bitbucket_token(credential=credential, loaders=loaders)
        is None
    )

    assert mock_credentials_update_credential_state.called is False
