from custom_exceptions import (
    CredentialAlreadyExists,
)
from db_model.credentials.types import (
    Credential,
)
from typing import (
    Any,
)


async def validate_credential_name_in_organization(
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
