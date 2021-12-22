from db_model import (
    TABLE,
)
from db_model.root_credentials.types import (
    RootCredentialItem,
)
from dynamodb import (
    historics,
    keys,
    operations,
)
import simplejson as json  # type: ignore


async def add(*, root_credential: RootCredentialItem) -> None:
    key_structure = TABLE.primary_key

    metadata_key = keys.build_key(
        facet=TABLE.facets["root_credentials_metadata"],
        values={
            "name": root_credential.group_name,
            "uuid": root_credential.id,
        },
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **json.loads(json.dumps(root_credential.metadata)),
    }

    historic_state = historics.build_historic(
        attributes=json.loads(json.dumps(root_credential.state)),
        historic_facet=TABLE.facets["root_credentials_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": root_credential.state.modified_date,
            "name": root_credential.group_name,
            "uuid": root_credential.id,
        },
        latest_facet=TABLE.facets["root_credential_state"],
    )

    items = (initial_metadata, *historic_state)
    await operations.batch_write_item(items=items, table=TABLE)
