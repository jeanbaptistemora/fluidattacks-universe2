from custom_exceptions import (
    CredentialAlreadyExists,
)
from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    Credentials,
    OauthGitlabSecret,
)
from db_model.enums import (
    CredentialType,
)


async def validate_credentials_name_in_organization(
    loaders: Dataloaders,
    organization_id: str,
    credentials_name: str,
) -> None:
    org_credentials: tuple[
        Credentials, ...
    ] = await loaders.organization_credentials.load(organization_id)
    credentials_names = {
        credentials.state.name.strip() for credentials in org_credentials
    }
    if credentials_name.strip() in credentials_names:
        raise CredentialAlreadyExists()


async def validate_credentials_oauth(
    loaders: Dataloaders,
    organization_id: str,
    user_email: str,
) -> None:
    org_credentials: tuple[
        Credentials, ...
    ] = await loaders.organization_credentials.load(organization_id)
    credentials = {
        credential.owner
        for credential in org_credentials
        if credential.state.type is CredentialType.OAUTH
        and isinstance(credential.state.secret, OauthGitlabSecret)
        and credential.owner.lower() == user_email.lower()
    }
    if credentials:
        raise CredentialAlreadyExists()
