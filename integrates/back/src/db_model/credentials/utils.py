from custom_exceptions import (
    InvalidCredentialSecret,
)
from db_model.credentials.types import (
    Credential,
    CredentialNewState,
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


def format_credential(item: Item) -> Credential:
    credential_type = CredentialType(item["state"]["type"])
    return Credential(
        id=item["id"],
        organization_id=item["organization_id"],
        owner=item["owner"],
        state=CredentialNewState(
            modified_by=item["state"]["modified_by"],
            modified_date=item["state"]["modified_date"],
            name=item["state"]["name"],
            secret=format_secret(credential_type, item["state"]["secret"]),
            type=credential_type,
        ),
    )


def validate_secret(state: CredentialNewState) -> None:
    if (
        state.type is CredentialType.SSH
        and not isinstance(state.secret, SshSecret)
    ) or (
        state.type is CredentialType.HTTPS
        and not isinstance(state.secret, (HttpsSecret, HttpsPatSecret))
    ):
        raise InvalidCredentialSecret()
