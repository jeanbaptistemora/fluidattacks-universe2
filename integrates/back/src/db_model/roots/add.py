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
    machine_execution_key = keys.build_key(
        facet=TABLE.facets["machine_git_root_execution"],
        values={"name": root.group_name, "uuid": root.id},
    )
    initial_machine_exectution = {
        key_structure.partition_key: machine_execution_key.partition_key,
        key_structure.sort_key: machine_execution_key.sort_key,
    }
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **json.loads(json.dumps(root.metadata)),
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

    items = (initial_metadata, initial_machine_exectution, *historic_state)

    if isinstance(root, GitRootItem):
        historic_cloning = historics.build_historic(
            attributes=json.loads(json.dumps(root.cloning)),
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
