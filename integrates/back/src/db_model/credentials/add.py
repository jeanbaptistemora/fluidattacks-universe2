from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
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
)
from db_model.credentials.utils import (
    validate_secret,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json  # type: ignore


async def add_new(*, credential: Credential) -> None:
    validate_secret(credential.state)
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
