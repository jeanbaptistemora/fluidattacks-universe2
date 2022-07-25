"""Data Access Layer to the Forces tables."""


from boto3.dynamodb.conditions import (
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_S3_FORCES_BUCKET,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import json
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
)
from s3 import (
    operations as s3_ops,
)
from settings import (
    LOGGING,
)
import tempfile
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


async def get_log_execution(group_name: str, execution_id: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        await s3_ops.download_file(
            FI_AWS_S3_FORCES_BUCKET,
            f"{group_name}/{execution_id}.log",
            file.name,
        )
        with open(file.name, encoding="utf-8") as reader:
            return reader.read()


async def get_vulns_execution(group_name: str, execution_id: str) -> Any:
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        await s3_ops.download_file(
            FI_AWS_S3_FORCES_BUCKET,
            f"{group_name}/{execution_id}.json",
            file.name,
        )
        with open(file.name, encoding="utf-8") as reader:
            return json.load(reader)


async def save_log_execution(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        FI_AWS_S3_FORCES_BUCKET,
        file_object,
        file_name,
    )


async def save_vulns_execution(file_object: object, file_name: str) -> None:
    await s3_ops.upload_memory_file(
        FI_AWS_S3_FORCES_BUCKET,
        file_object,
        file_name,
    )


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
