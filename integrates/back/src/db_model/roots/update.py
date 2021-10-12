from back.src.dynamodb import (
    keys,
)
from db_model import (
    TABLE,
)
from db_model.roots.types import (
    GitRootCloning,
    GitRootState,
    IPRootState,
    URLRootState,
)
from dynamodb import (
    historics,
    operations,
)
import simplejson as json  # type: ignore
from typing import (
    Union,
)


async def update_root_state(
    *,
    group_name: str,
    root_id: str,
    state: Union[GitRootState, IPRootState, URLRootState],
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=json.loads(json.dumps(state)),
        historic_facet=TABLE.facets["git_root_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": state.modified_date,
            "name": group_name,
            "uuid": root_id,
        },
        latest_facet=TABLE.facets["git_root_state"],
    )

    await operations.batch_write_item(items=historic, table=TABLE)


async def update_git_root_machine_execution(
    group_name: str,
    root_id: str,
    finding_code: str,
    queue_date: str,
    batch_id: str,
) -> None:
    key_structure = TABLE.primary_key
    current_facet = TABLE.facets["machine_git_root_execution"]
    key = keys.build_key(
        facet=current_facet,
        values={
            "uuid": root_id,
            "name": group_name,
            "finding_code": finding_code,
        },
    )
    execution = {
        key_structure.partition_key: key.partition_key,
        key_structure.sort_key: key.sort_key,
        "queue_date": queue_date,
        "job_id": batch_id,
        "finding_code": finding_code,
    }
    await operations.batch_write_item(items=(execution,), table=TABLE)


async def update_git_root_cloning(
    *, cloning: GitRootCloning, group_name: str, root_id: str
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=json.loads(json.dumps(cloning)),
        historic_facet=TABLE.facets["git_root_historic_cloning"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": cloning.modified_date,
            "name": group_name,
            "uuid": root_id,
        },
        latest_facet=TABLE.facets["git_root_cloning"],
    )

    await operations.batch_write_item(items=historic, table=TABLE)
