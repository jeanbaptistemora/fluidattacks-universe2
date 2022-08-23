"""Data Access Layer to the Forces tables."""


from boto3.dynamodb.conditions import (
    Key,
)
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
    AsyncIterator,
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


async def get_execution(group_name: str, execution_id: str) -> Any:
    key_condition_expresion = {
        "execution_id": execution_id,
        "subscription": group_name,
    }
    result = await dynamodb_ops.get_item(
        TABLE_NAME, {"Key": key_condition_expresion}
    )
    if result:
        if "accepted" not in result["vulnerabilities"]:
            result["vulnerabilities"]["accepted"] = []
        if "open" not in result["vulnerabilities"]:
            result["vulnerabilities"]["open"] = []
        if "closed" not in result["vulnerabilities"]:
            result["vulnerabilities"]["closed"] = []
        # Compatibility with old API
        result["project_name"] = result.get("subscription")
        result["group_name"] = result.get("subscription")
        return result
    return {}


async def yield_executions(
    group_name: str,
    group_name_key: str,
) -> AsyncIterator[Any]:
    """Lazy iterator over the executions of a group"""
    key_condition_expresion = Key("subscription").eq(group_name)

    query_params = {
        "KeyConditionExpression": key_condition_expresion,
        "IndexName": "date",
        "ScanIndexForward": False,
    }
    results = await dynamodb_ops.query(TABLE_NAME, query_params)
    for result in results:
        if "accepted" not in result["vulnerabilities"]:
            result["vulnerabilities"]["accepted"] = []
        if "open" not in result["vulnerabilities"]:
            result["vulnerabilities"]["open"] = []
        if "closed" not in result["vulnerabilities"]:
            result["vulnerabilities"]["closed"] = []
        result[f"{group_name_key}"] = result.get("subscription")
        # Exception: WF(AsyncIterator is subtype of iterator)
        yield result  # NOSONAR
