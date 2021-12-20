from boto3.dynamodb.conditions import (
    Attr,
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
    keys,
    operations,
)
import simplejson as json  # type: ignore
from typing import (
    Union,
)


async def update_root_state(
    *,
    current_value: Union[GitRootState, IPRootState, URLRootState],
    group_name: str,
    root_id: str,
    state: Union[GitRootState, IPRootState, URLRootState],
) -> None:
    key_structure = TABLE.primary_key
    latest_facet, historic_facet = (
        (
            TABLE.facets["git_root_state"],
            TABLE.facets["git_root_historic_state"],
        )
        if isinstance(state, GitRootState)
        else (
            TABLE.facets["ip_root_state"],
            TABLE.facets["ip_root_historic_state"],
        )
        if isinstance(state, IPRootState)
        else (
            TABLE.facets["url_root_state"],
            TABLE.facets["url_root_historic_state"],
        )
    )
    latest, historic = historics.build_historic(
        attributes=json.loads(json.dumps(state)),
        historic_facet=historic_facet,
        key_structure=key_structure,
        key_values={
            "iso8601utc": state.modified_date,
            "name": group_name,
            "uuid": root_id,
        },
        latest_facet=latest_facet,
    )
    await operations.put_item(
        condition_expression=(
            Attr("modified_date").eq(current_value.modified_date)
        ),
        facet=latest_facet,
        item=latest,
        table=TABLE,
    )
    await operations.put_item(facet=historic_facet, item=historic, table=TABLE)


async def update_git_root_machine_execution(
    group_name: str,
    root_id: str,
    finding_code: str,
    queue_date: str,
    batch_id: str,
) -> None:
    key_structure = TABLE.primary_key
    key = keys.build_key(
        facet=TABLE.facets["machine_git_root_execution"],
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
    await operations.put_item(
        facet=TABLE.facets["machine_git_root_execution"],
        item=execution,
        table=TABLE,
    )


async def update_git_root_cloning(
    *,
    cloning: GitRootCloning,
    current_value: GitRootCloning,
    group_name: str,
    root_id: str,
) -> None:
    key_structure = TABLE.primary_key
    latest, historic = historics.build_historic(
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

    await operations.put_item(
        condition_expression=(
            Attr("modified_date").eq(current_value.modified_date)
        ),
        facet=TABLE.facets["git_root_cloning"],
        item=latest,
        table=TABLE,
    )
    await operations.put_item(
        facet=TABLE.facets["git_root_historic_cloning"],
        item=historic,
        table=TABLE,
    )
