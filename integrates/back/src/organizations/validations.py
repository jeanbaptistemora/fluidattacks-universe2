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
    new_credential: Credential,
) -> None:
    org_credentials: tuple[
        Credential, ...
    ] = await loaders.organization_credentials_new.load(
        new_credential.organization_id
    )
    credential_names = {
        credential.state.name for credential in org_credentials
    }
    if new_credential.state.name in credential_names:
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
