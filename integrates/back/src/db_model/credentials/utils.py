from custom_exceptions import (
    InvalidCredentialSecret,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Union,
)


def format_secret(
    credential_type: CredentialType, item: Item
) -> Union[HttpsPatSecret, HttpsSecret, SshSecret]:
    if credential_type is CredentialType.HTTPS:
        if "token" in item:
            return HttpsPatSecret(token=item["token"])

        return HttpsSecret(
            user=item["user"],
            password=item["password"],
        )

    return SshSecret(key=item["key"])


def format_credential(item: Item) -> Credentials:
    credential_type = CredentialType(item["state"]["type"])
    return Credentials(
        id=item["id"],
        organization_id=item["organization_id"],
        owner=item["owner"],
        state=CredentialsState(
            modified_by=item["state"]["modified_by"],
            modified_date=datetime.fromisoformat(
                item["state"]["modified_date"]
            ),
            name=item["state"]["name"],
            is_pat=item["state"].get("is_pat", False),
            azure_organization=item["state"].get("azure_organization", None),
            secret=format_secret(credential_type, item["state"]["secret"]),
            type=credential_type,
        ),
    )


def validate_secret(state: CredentialsState) -> None:
    if state.is_pat and (
        state.type is not CredentialType.HTTPS
        or not isinstance(state.secret, HttpsPatSecret)
        or state.azure_organization is None
    ):
        raise InvalidCredentialSecret()
    if (
        state.type is CredentialType.SSH
        and not isinstance(state.secret, SshSecret)
    ) or (
        state.type is CredentialType.HTTPS
        and not isinstance(state.secret, (HttpsSecret, HttpsPatSecret))
    ):
        raise InvalidCredentialSecret()


def filter_pat_credentials(
    credentials: tuple[Credentials, ...],
) -> tuple[Credentials, ...]:
    return tuple(
        credential
        for credential in credentials
        if credential.state.is_pat
        and credential.state.azure_organization is not None
    )
