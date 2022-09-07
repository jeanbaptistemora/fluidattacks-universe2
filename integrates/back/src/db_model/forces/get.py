# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .constants import (
    GSI_2_FACET,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    Iterable,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    ExecutionNotFound,
)
from db_model import (
    TABLE,
)
from db_model.forces.types import (
    ForcesExecution,
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


async def _get_executions(
    *, group_name: str, limit: Optional[int] = None
) -> tuple[ForcesExecution, ...]:
    if limit is None:
        paginate = False
        primary_key = keys.build_key(
            facet=TABLE.facets["forces_execution"],
            values={"name": group_name},
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
                "name": group_name,
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
        limit=limit,
        table=TABLE,
        index=index,
    )
    return tuple(format_forces_execution(item) for item in response.items)


async def _get_execution(
    *, group_name: str, execution_id: str
) -> ForcesExecution:
    primary_key = keys.build_key(
        facet=TABLE.facets["forces_execution"],
        values={"name": group_name, "id": execution_id},
    )

    item = await operations.get_item(
        facets=(TABLE.facets["forces_execution"],),
        key=primary_key,
        table=TABLE,
    )
    if not item:
        raise ExecutionNotFound()

    return format_forces_execution(item)


class ForcesExecutionLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, forces_keys: Iterable[tuple[str, str]]
    ) -> tuple[ForcesExecution, ...]:
        return await collect(
            tuple(
                _get_execution(
                    group_name=group_name, execution_id=execution_id
                )
                for group_name, execution_id in forces_keys
            )
        )


class ForcesExecutionsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, forces_keys: Iterable[tuple[str, Optional[int]]]
    ) -> tuple[tuple[ForcesExecution, ...], ...]:
        return await collect(
            tuple(
                _get_executions(group_name=group_name, limit=limit)
                for group_name, limit in forces_keys
            )
        )
