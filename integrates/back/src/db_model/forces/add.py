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

    forces_execution_key = keys.build_key(
        facet=TABLE.facets["forces_execution"],
        values={
            "name": forces_execution.group_name,
            "id": forces_execution.id,
        },
    )

    forces_execution_item = {
        key_structure.partition_key: forces_execution_key.partition_key,
        key_structure.sort_key: forces_execution_key.sort_key,
        **format_forces_item(forces_execution),
    }

    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["forces_execution"],
            item=forces_execution_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise ExecutionAlreadyCreated() from ex
