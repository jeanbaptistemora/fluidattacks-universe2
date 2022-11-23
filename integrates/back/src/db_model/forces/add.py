from .constants import (
    GSI_2_FACET,
)
from .types import (
    ForcesExecution,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    ExecutionAlreadyCreated,
)
from db_model import (
    TABLE,
)
from db_model.forces.utils import (
    format_forces_item,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)


async def add(*, forces_execution: ForcesExecution) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    primary_key = keys.build_key(
        facet=TABLE.facets["forces_execution"],
        values={
            "id": forces_execution.id,
            "name": forces_execution.group_name,
        },
    )
    gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "execution_date": forces_execution.execution_date,
            "name": forces_execution.group_name,
        },
    )
    item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        **format_forces_item(forces_execution),
    }
    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["forces_execution"],
            item=item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise ExecutionAlreadyCreated() from ex
