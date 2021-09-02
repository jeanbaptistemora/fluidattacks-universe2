from db_model import (
    TABLE,
)
from db_model.roots.types import (
    GitRootItem,
    RootItem,
)
from dynamodb import (
    historics,
    keys,
    operations,
)
import simplejson as json  # type: ignore


async def add(*, root: RootItem) -> None:
    key_structure = TABLE.primary_key

    metadata_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": root.group_name, "uuid": root.id},
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **dict(root.metadata._asdict()),
    }

    historic_state = historics.build_historic(
        attributes=json.loads(json.dumps(root.state)),
        historic_facet=TABLE.facets["git_root_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": root.state.modified_date,
            "name": root.group_name,
            "uuid": root.id,
        },
        latest_facet=TABLE.facets["git_root_state"],
    )

    items = (initial_metadata, *historic_state)

    if isinstance(root, GitRootItem):
        historic_cloning = historics.build_historic(
            attributes=dict(root.cloning._asdict()),
            historic_facet=TABLE.facets["git_root_historic_cloning"],
            key_structure=key_structure,
            key_values={
                "iso8601utc": root.cloning.modified_date,
                "name": root.group_name,
                "uuid": root.id,
            },
            latest_facet=TABLE.facets["git_root_cloning"],
        )
        await operations.batch_write_item(
            items=(*items, *historic_cloning), table=TABLE
        )
    else:
        await operations.batch_write_item(items=items, table=TABLE)
