from .constants import (
    GSI_2_FACET,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from db_model.forces.types import (
    ForcesExecution,
    ForcesExecutionRequest,
    GroupForcesExecutionsRequest,
)
from db_model.forces.utils import (
    format_forces_execution,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Optional,
)


async def _get_group_executions(
    *, request: GroupForcesExecutionsRequest
) -> list[ForcesExecution]:
    if request.limit is None:
        paginate = False
        primary_key = keys.build_key(
            facet=TABLE.facets["forces_execution"],
            values={"name": request.group_name},
        )
        index = TABLE.indexes["inverted_index"]
        key_structure = TABLE.primary_key
        condition_expression = Key(key_structure.sort_key).eq(
            primary_key.sort_key
        ) & Key(key_structure.partition_key).begins_with(
            primary_key.partition_key
        )
    else:
        paginate = True
        facet = GSI_2_FACET
        primary_key = keys.build_key(
            facet=facet,
            values={
                "name": request.group_name,
            },
        )
        index = TABLE.indexes["gsi_2"]
        key_structure = index.primary_key
        condition_expression = Key(key_structure.partition_key).eq(
            primary_key.partition_key
        ) & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
    response = await operations.query(
        paginate=paginate,
        condition_expression=condition_expression,
        facets=(TABLE.facets["forces_execution"],),
        limit=request.limit,
        table=TABLE,
        index=index,
    )
    return [format_forces_execution(item) for item in response.items]


async def _get_executions(
    *, requests: list[ForcesExecutionRequest]
) -> list[Optional[ForcesExecution]]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["forces_execution"],
            values={"name": request.group_name, "id": request.execution_id},
        )
        for request in requests
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    response = {
        ForcesExecutionRequest(
            group_name=execution.group_name, execution_id=execution.id
        ): execution
        for execution in [format_forces_execution(item) for item in items]
    }
    return list(response[request] for request in requests)


class ForcesExecutionLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: list[ForcesExecutionRequest]
    ) -> list[Optional[ForcesExecution]]:
        return await _get_executions(requests=requests)


class GroupForcesExecutionsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: list[GroupForcesExecutionsRequest]
    ) -> list[list[ForcesExecution]]:
        return list(
            await collect(
                _get_group_executions(request=request) for request in requests
            )
        )
