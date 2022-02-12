import botocore
from contextlib import (
    suppress,
)
from db_model import (
    TABLE,
)
from db_model.roots.types import (
    GitRootItem,
    RootItem,
    RootMachineExecutionItem,
)
from dynamodb import (
    historics,
    keys,
    operations,
)
import simplejson as json  # type: ignore


async def add(*, root: RootItem) -> None:
    items = []
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": root.group_name, "uuid": root.id},
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        "state": json.loads(json.dumps(root.state)),
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
    items.extend(historic_state)

    if isinstance(root, GitRootItem):
        initial_metadata["cloning"] = json.loads(json.dumps(root.cloning))
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
        items.extend(historic_cloning)
    items.append(initial_metadata)

    await operations.batch_write_item(items=items, table=TABLE)


async def add_machine_execution(
    root_id: str,
    execution: RootMachineExecutionItem,
) -> bool:
    key_structure = TABLE.primary_key
    machine_execution_key = keys.build_key(
        facet=TABLE.facets["machine_git_root_execution_new"],
        values={"uuid": root_id, "job_id": execution.job_id},
    )
    machine_exectution = {
        key_structure.partition_key: machine_execution_key.partition_key,
        key_structure.sort_key: machine_execution_key.sort_key,
        "created_at": execution.created_at,
        "started_at": execution.started_at,
        "stopped_at": execution.stopped_at,
        "findings_executed": execution.findings_executed,
        "queue": execution.queue,
        "name": execution.name,
        "commit": execution.commit,
    }
    with suppress(botocore.exceptions.ClientError):
        await operations.batch_write_item(
            items=(machine_exectution,), table=TABLE
        )
        return True

    return False
