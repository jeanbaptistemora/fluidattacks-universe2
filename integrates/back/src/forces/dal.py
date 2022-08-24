"""Data Access Layer to the Forces tables."""


from botocore.exceptions import (
    ClientError,
)
from db_model.forces.types import (
    ForcesExecution,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
)
from newutils.forces import (
    format_forces_item,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME = "FI_forces"


async def add_execution(group_name: str, **execution_attributes: Any) -> bool:
    """Add/creates an execution of forces."""
    success = False
    try:
        execution_attributes["date"] = datetime_utils.get_as_str(
            execution_attributes["date"],
            date_format="%Y-%m-%dT%H:%M:%S.%f%z",
            zone="UTC",
        )
        execution_attributes["subscription"] = group_name
        execution_attributes = dynamodb_ops.serialize(execution_attributes)
        success = await dynamodb_ops.put_item(TABLE_NAME, execution_attributes)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def add_execution_typed(force_execution: ForcesExecution) -> None:
    item = format_forces_item(force_execution)
    await add_execution(force_execution.group_name, **item)
