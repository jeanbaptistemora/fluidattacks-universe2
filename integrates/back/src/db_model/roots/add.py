import botocore
from contextlib import (
    suppress,
)
from db_model import (
    TABLE,
)
from db_model.roots.constants import (
    ORG_INDEX_METADATA,
)
from db_model.roots.types import (
    GitRoot,
    MachineFindingResult,
    Root,
    RootEnvironmentUrl,
    RootMachineExecution,
    Secret,
)
from db_model.utils import (
    get_as_utc_iso_format,
    serialize,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json


async def add(*, root: Root) -> None:
    items = []
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": root.group_name, "uuid": root.id},
    )
    gsi_2_index = TABLE.indexes["gsi_2"]
    gsi_2_key = keys.build_key(
        facet=ORG_INDEX_METADATA,
        values={"name": root.organization_name, "uuid": root.id},
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        **json.loads(json.dumps(root, default=serialize)),
    }
    items.append(initial_metadata)

    state_key = keys.build_key(
        facet=TABLE.facets["git_root_historic_state"],
        values={
            "uuid": root.id,
            "iso8601utc": get_as_utc_iso_format(root.state.modified_date),
        },
    )
    historic_state_item = {
        key_structure.partition_key: state_key.partition_key,
        key_structure.sort_key: state_key.sort_key,
        **json.loads(json.dumps(root.state, default=serialize)),
    }
    items.append(historic_state_item)

    if isinstance(root, GitRoot):
        cloning_key = keys.build_key(
            facet=TABLE.facets["git_root_historic_cloning"],
            values={
                "uuid": root.id,
                "iso8601utc": get_as_utc_iso_format(
                    root.cloning.modified_date
                ),
            },
        )
        historic_cloning_item = {
            key_structure.partition_key: cloning_key.partition_key,
            key_structure.sort_key: cloning_key.sort_key,
            **json.loads(json.dumps(root.cloning, default=serialize)),
        }
        items.append(historic_cloning_item)

    await operations.batch_put_item(items=tuple(items), table=TABLE)


async def add_machine_execution(
    root_id: str,
    execution: RootMachineExecution,
) -> bool:
    key_structure = TABLE.primary_key
    machine_execution_key = keys.build_key(
        facet=TABLE.facets["machine_git_root_execution"],
        values={"uuid": root_id, "job_id": execution.job_id},
    )
    if len(execution.findings_executed) > 0 and isinstance(
        execution.findings_executed[0], MachineFindingResult
    ):
        findings = [
            {
                "finding": item.finding,
                "modified": item.modified,
                "open": item.open,
            }
            for item in execution.findings_executed
        ]
    else:
        findings = execution.findings_executed  # type: ignore

    machine_exectution = {
        key_structure.partition_key: machine_execution_key.partition_key,
        key_structure.sort_key: machine_execution_key.sort_key,
        "created_at": get_as_utc_iso_format(execution.created_at),
        "started_at": get_as_utc_iso_format(execution.started_at)
        if execution.started_at
        else None,
        "stopped_at": get_as_utc_iso_format(execution.stopped_at)
        if execution.stopped_at
        else None,
        "findings_executed": findings,
        "queue": execution.queue,
        "name": execution.name,
        "commit": execution.commit,
        "status": execution.status,
    }
    with suppress(botocore.exceptions.ClientError):
        await operations.batch_put_item(
            items=(machine_exectution,), table=TABLE
        )
        return True

    return False


async def add_secret(
    root_id: str,
    secret: Secret,
) -> bool:
    key_structure = TABLE.primary_key
    secret_key = keys.build_key(
        facet=TABLE.facets["root_secret"],
        values={"uuid": root_id, "key": secret.key},
    )
    secret_item = {
        key_structure.partition_key: secret_key.partition_key,
        key_structure.sort_key: secret_key.sort_key,
        "key": secret.key,
        "value": secret.value,
        "description": secret.description,
    }
    with suppress(botocore.exceptions.ClientError):
        await operations.batch_put_item(items=(secret_item,), table=TABLE)
        return True

    return False


async def add_root_environment_secret(
    url_id: str,
    secret: Secret,
) -> bool:
    key_structure = TABLE.primary_key
    secret_key = keys.build_key(
        facet=TABLE.facets["root_environment_secret"],
        values={"hash": url_id, "key": secret.key},
    )
    secret_item = {
        key_structure.partition_key: secret_key.partition_key,
        key_structure.sort_key: secret_key.sort_key,
        "key": secret.key,
        "value": secret.value,
        "description": secret.description,
        "created_at": get_as_utc_iso_format(secret.created_at)
        if secret.created_at
        else None,
    }
    with suppress(botocore.exceptions.ClientError):
        await operations.batch_put_item(items=(secret_item,), table=TABLE)
        return True

    return False


async def add_root_environment_url(
    root_id: str,
    url: RootEnvironmentUrl,
) -> bool:
    key_structure = TABLE.primary_key
    url_key = keys.build_key(
        facet=TABLE.facets["root_environment_url"],
        values={"uuid": root_id, "hash": url.id},
    )
    url_item = {
        key_structure.partition_key: url_key.partition_key,
        key_structure.sort_key: url_key.sort_key,
        "url": url.url,
        "created_at": get_as_utc_iso_format(url.created_at)
        if url.created_at
        else None,
        "type": url.url_type.value,
        "cloud_name": url.cloud_name.value if url.cloud_name else None,
    }
    with suppress(botocore.exceptions.ClientError):
        await operations.batch_put_item(items=(url_item,), table=TABLE)
        return True

    return False
