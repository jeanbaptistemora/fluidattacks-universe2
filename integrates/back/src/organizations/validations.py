from custom_exceptions import (
    CredentialAlreadyExists,
    StakeholderIsNotCredentialsOwner,
)
from db_model.credentials.types import (
    Credential,
    CredentialRequest,
)
from typing import (
    Any,
)


async def validate_credentials_name_in_organization(
    loaders: Any,
    organization_id: str,
    credentials_name: str,
) -> None:
    org_credentials: tuple[
        Credential, ...
    ] = await loaders.organization_credentials_new.load(organization_id)
    credentials_names = {
        credentials.state.name for credentials in org_credentials
    }
    if credentials_name in credentials_names:
        raise CredentialAlreadyExists()


async def validate_stakeholder_is_credentials_owner(
    loaders: Any,
    credentials_id: str,
    organization_id: str,
    stakeholder: str,
) -> None:
    credentials: Credential = await loaders.credential_new.load(
        CredentialRequest(
            id=credentials_id,
            organization_id=organization_id,
        )
    )

    if credentials.owner != stakeholder:
        raise StakeholderIsNotCredentialsOwner()
