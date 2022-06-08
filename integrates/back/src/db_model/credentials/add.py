from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    InvalidCredentialSecret,
    RepeatedCredential,
)
from db_model import (
    TABLE,
)
from db_model.credentials.constants import (
    OWNER_INDEX_FACET,
)
from db_model.credentials.types import (
    Credential,
    CredentialItem,
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
)
from dynamodb import (
    historics,
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json  # type: ignore


async def add(*, credential: CredentialItem) -> None:
    key_structure = TABLE.primary_key

    metadata_key = keys.build_key(
        facet=TABLE.facets["credentials_metadata"],
        values={
            "name": credential.group_name,
            "uuid": credential.id,
        },
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **json.loads(json.dumps(credential.metadata)),
    }

    historic_state = historics.build_historic(
        attributes=json.loads(json.dumps(credential.state)),
        historic_facet=TABLE.facets["credentials_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": credential.state.modified_date,
            "name": credential.group_name,
            "uuid": credential.id,
        },
        latest_facet=TABLE.facets["credentials_state"],
    )

    items = (initial_metadata, *historic_state)
    await operations.batch_put_item(items=items, table=TABLE)


async def add_new(*, credential: Credential) -> None:
    if (
        credential.state.type is CredentialType.SSH
        and not isinstance(credential.state.secret, SshSecret)
    ) or (
        credential.state.type is CredentialType.HTTPS
        and not isinstance(
            credential.state.secret, (HttpsSecret, HttpsPatSecret)
        )
    ):
        raise InvalidCredentialSecret()

    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["credentials_new_metadata"],
        values={
            "organization_id": credential.organization_id,
            "id": credential.id,
        },
    )
    gsi_2_index = TABLE.indexes["gsi_2"]
    gsi_2_key = keys.build_key(
        facet=OWNER_INDEX_FACET,
        values={
            "owner": credential.owner,
            "id": credential.id,
        },
    )
    item = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        **json.loads(json.dumps(credential)),
    }
    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["credentials_new_metadata"],
            item=item,
            table=TABLE,
        )

    except ConditionalCheckFailedException as ex:
        raise RepeatedCredential() from ex
