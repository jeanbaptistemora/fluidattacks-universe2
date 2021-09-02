"""Data Access Layer to the Forces tables."""


import aioboto3
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_S3_FORCES_BUCKET,
)
from datetime import (
    datetime,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from dynamodb.model import (
    get_agent_token,
    update_group_agent_token,
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
    Optional,
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
    key_condition_expresion = Key("execution_id").eq(execution_id) & Key(
        "subscription"
    ).eq(group_name)

    async with aioboto3.resource(**dynamodb_ops.RESOURCE_OPTIONS) as resource:
        table = await resource.Table(TABLE_NAME)
        results = await table.query(
            KeyConditionExpression=key_condition_expresion
        )
        if results:
            result = results["Items"][0]
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
        return dict()


async def get_log_execution(group_name: str, execution_id: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        await s3_ops.download_file(
            FI_AWS_S3_FORCES_BUCKET,
            f"{group_name}/{execution_id}.log",
            file.name,
        )
        with open(file.name) as reader:
            return reader.read()


async def get_secret_token(group_name: str) -> Optional[str]:
    try:
        return await get_agent_token(group_name=group_name)
    except ClientError as error:
        LOGGER.exception(error, extra={"extra": locals()})
        return None


async def get_vulns_execution(group_name: str, execution_id: str) -> Any:
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        await s3_ops.download_file(
            FI_AWS_S3_FORCES_BUCKET,
            f"{group_name}/{execution_id}.json",
            file.name,
        )
        with open(file.name) as reader:
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


async def update_secret_token(group_name: str, secret: str) -> bool:
    try:
        await update_group_agent_token(
            group_name=group_name,
            agent_token=secret,
        )
    except ClientError as error:
        LOGGER.exception(error, extra={"extra": locals()})
        return False
    return True


async def yield_executions(
    group_name: str,
    group_name_key: str,
    from_date: datetime,
    to_date: datetime,
) -> AsyncIterator[Any]:
    """Lazy iterator over the executions of a group"""
    key_condition_expresion = Key("subscription").eq(group_name)
    filter_expression = Attr("date").gte(from_date.isoformat()) & Attr(
        "date"
    ).lte(to_date.isoformat())

    async with aioboto3.resource(**dynamodb_ops.RESOURCE_OPTIONS) as resource:
        table = await resource.Table(TABLE_NAME)
        query_params = {
            "KeyConditionExpression": key_condition_expresion,
            "FilterExpression": filter_expression,
        }
        has_more = True
        while has_more:
            results = await table.query(**query_params)
            for result in results["Items"]:
                if "accepted" not in result["vulnerabilities"]:
                    result["vulnerabilities"]["accepted"] = []
                if "open" not in result["vulnerabilities"]:
                    result["vulnerabilities"]["open"] = []
                if "closed" not in result["vulnerabilities"]:
                    result["vulnerabilities"]["closed"] = []
                result[f"{group_name_key}"] = result.get("subscription")
                # Exception: WF(AsyncIterator is subtype of iterator)
                yield result  # NOSONAR
            if results.get("LastEvaluatedKey", None):
                query_params["ExclusiveStartKey"] = results.get(
                    "LastEvaluatedKey"
                )
            has_more = results.get("LastEvaluatedKey", False)
