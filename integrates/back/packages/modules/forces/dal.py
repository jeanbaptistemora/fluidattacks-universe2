"""Data Access Layer to the Forces tables."""


import json
import logging
import logging.config
import tempfile
from datetime import datetime
from typing import (
    Any,
    AsyncIterator,
    Optional,
    cast,
)

import aioboto3
import aioextensions
import boto3
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from botocore.exceptions import ClientError

from context import (
    FI_AWS_S3_FORCES_BUCKET,
    FI_AWS_SECRETSMANAGER_ACCESS_KEY,
    FI_AWS_SECRETSMANAGER_SECRET_KEY,
    FI_AWS_SESSION_TOKEN,
)
from dynamodb import operations_legacy as dynamodb_ops
from newutils import datetime as datetime_utils
from s3 import operations as s3_ops
from settings import LOGGING


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME = "FI_forces"


async def create_execution(
    project_name: str, **execution_attributes: Any
) -> bool:
    """Create an execution of forces."""
    success = False
    try:
        execution_attributes["date"] = datetime_utils.get_as_str(
            execution_attributes["date"],
            date_format="%Y-%m-%dT%H:%M:%S.%f%z",
            zone="UTC",
        )
        execution_attributes["subscription"] = project_name
        execution_attributes = dynamodb_ops.serialize(execution_attributes)
        success = await dynamodb_ops.put_item(TABLE_NAME, execution_attributes)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def get_execution(project_name: str, execution_id: str) -> Any:
    key_condition_expresion = Key("execution_id").eq(execution_id) & Key(
        "subscription"
    ).eq(project_name)

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
            result["project_name"] = result.get("subscription")
            return result
        return dict()


async def get_log_execution(project_name: str, execution_id: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        await s3_ops.download_file(
            FI_AWS_S3_FORCES_BUCKET,
            f"{project_name}/{execution_id}.log",
            file.name,
        )
        with open(file.name) as reader:
            return reader.read()


async def get_secret_token(project_name: str) -> Optional[str]:
    client = boto3.client(
        "secretsmanager",
        aws_access_key_id=FI_AWS_SECRETSMANAGER_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_SECRETSMANAGER_SECRET_KEY,
        aws_session_token=FI_AWS_SESSION_TOKEN,
    )
    try:
        response = await aioextensions.in_thread(
            client.get_secret_value,
            SecretId=f"forces_token_{project_name}",
        )
    except ClientError as error:
        LOGGER.exception(error, extra={"extra": locals()})
        return None
    return cast(str, response.get("SecretString"))


async def get_vulns_execution(project_name: str, execution_id: str) -> Any:
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        await s3_ops.download_file(
            FI_AWS_S3_FORCES_BUCKET,
            f"{project_name}/{execution_id}.json",
            file.name,
        )
        with open(file.name) as reader:
            return json.load(reader)


async def save_log_execution(file_object: object, file_name: str) -> bool:
    return await s3_ops.upload_memory_file(
        FI_AWS_S3_FORCES_BUCKET,
        file_object,
        file_name,
    )


async def save_vulns_execution(file_object: object, file_name: str) -> bool:
    return await s3_ops.upload_memory_file(
        FI_AWS_S3_FORCES_BUCKET,
        file_object,
        file_name,
    )


async def update_secret_token(project_name: str, secret: str) -> bool:
    client = boto3.client(
        "secretsmanager",
        aws_access_key_id=FI_AWS_SECRETSMANAGER_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_SECRETSMANAGER_SECRET_KEY,
        aws_session_token=FI_AWS_SESSION_TOKEN,
    )
    try:
        await aioextensions.in_thread(
            client.put_secret_value,
            SecretId=f"forces_token_{project_name}",
            SecretString=secret,
        )
    except ClientError as error:
        LOGGER.exception(error, extra={"extra": locals()})
        return False
    return True


async def yield_executions(
    project_name: str,
    from_date: datetime,
    to_date: datetime,
) -> AsyncIterator[Any]:
    """ Lazy iterator over the executions of a project """
    key_condition_expresion = Key("subscription").eq(project_name)
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
                result["project_name"] = result.get("subscription")
                yield result
            if results.get("LastEvaluatedKey", None):
                query_params["ExclusiveStartKey"] = results.get(
                    "LastEvaluatedKey"
                )
            has_more = results.get("LastEvaluatedKey", False)
