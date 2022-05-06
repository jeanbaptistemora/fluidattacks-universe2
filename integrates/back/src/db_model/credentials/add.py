from db_model import (
    TABLE,
)
from db_model.credentials.types import (
    CredentialItem,
)
from dynamodb import (
    historics,
    keys,
    operations,
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
