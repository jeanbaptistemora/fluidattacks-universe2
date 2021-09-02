import aioboto3
from boto3.dynamodb.conditions import (
    Equals,
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_S3_BUCKET,
)
from custom_types import (
    DynamoDelete as DynamoDeleteType,
    Finding as FindingType,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from newutils.utils import (
    duplicate_dict_keys,
)
from s3 import (
    operations as s3_ops,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Set,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "FI_findings"


def _escape_alnum(string: str) -> str:
    """Removes non-alphanumeric characters from a string"""
    return "".join([char for char in string if char.isalnum()])


async def add(
    finding_id: str, group_name: str, finding_attrs: Dict[str, FindingType]
) -> bool:
    success = False
    try:
        finding_attrs.update(
            {"finding_id": finding_id, "project_name": group_name}
        )
        success = await dynamodb_ops.put_item(TABLE_NAME, finding_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def download_evidence(file_name: str, file_path: str) -> None:
    await s3_ops.download_file(FI_AWS_S3_BUCKET, file_name, file_path)


async def get(
    finding_id: str, table: aioboto3.session.Session.client
) -> Dict[str, FindingType]:
    response = await table.get_item(Key={"finding_id": finding_id})
    return cast(Dict[str, FindingType], response.get("Item", {}))


async def get_attributes(
    finding_id: str, attributes: List[str]
) -> Dict[str, FindingType]:
    """Get a group of attributes of a finding."""
    finding_attrs: Dict[str, FindingType] = {}
    item_attrs = {"KeyConditionExpression": Key("finding_id").eq(finding_id)}
    if attributes:
        projection = ",".join(attributes)
        item_attrs.update({"ProjectionExpression": projection})
    response_item = cast(
        List[Dict[str, FindingType]],
        await dynamodb_ops.query(TABLE_NAME, item_attrs),
    )
    if response_item:
        finding_attrs = response_item[0]
    return finding_attrs


async def get_finding(finding_id: str) -> Dict[str, FindingType]:
    """Retrieve all attributes from a finding"""
    response = {}
    query_attrs = {
        "KeyConditionExpression": Key("finding_id").eq(finding_id),
        "Limit": 1,
    }
    response_items = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    if response_items:
        response = response_items[0]
        # Compatibility with old API
        if response["project_name"] is not None:
            response = duplicate_dict_keys(
                response, "group_name", "project_name"
            )
    return response


async def get_findings_by_group(
    group_name: str, attrs: Optional[Set[str]] = None
) -> List[Dict[str, Any]]:
    key_exp: Equals = Key("project_name").eq(group_name.lower())
    query_attrs = {
        "IndexName": "project_findings",
        "KeyConditionExpression": key_exp,
    }
    if attrs:
        query_attrs["ProjectionExpression"] = ",".join(attrs)
    return await dynamodb_ops.query(TABLE_NAME, query_attrs)


async def list_append(
    finding_id: str, attr: str, data: List[FindingType]
) -> bool:
    """
    Adds elements to the end of a list attribute

    :param finding_id: id of the finding to update
    :param attr: attribute name
    :param data: list with the elements to append
    """
    success = False
    try:
        update_attrs = {
            "Key": {"finding_id": finding_id},
            "UpdateExpression": f"SET {attr} = list_append({attr}, :data)",
            "ExpressionAttributeValues": {":data": data},
        }
        success = await dynamodb_ops.update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def remove_evidence(file_name: str) -> bool:
    await s3_ops.remove_file(FI_AWS_S3_BUCKET, file_name)
    return True


async def save_evidence(file_object: object, file_name: str) -> bool:
    return await s3_ops.upload_memory_file(
        FI_AWS_S3_BUCKET, file_object, file_name
    )


async def search_evidence(file_name: str) -> List[str]:
    return await s3_ops.list_files(FI_AWS_S3_BUCKET, file_name)


async def update(finding_id: str, data: Dict[str, FindingType]) -> bool:
    success = False
    set_expression = ""
    remove_expression = ""
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f"{attr}, "
        else:
            set_expression += f"{attr} = :{_escape_alnum(attr)}, "
            expression_values.update({f":{_escape_alnum(attr)}": value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        "Key": {"finding_id": finding_id},
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }
    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})

    try:
        success = await dynamodb_ops.update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def delete(finding_id: str) -> bool:
    """Delete a finding"""
    resp = False
    try:
        delete_attrs = DynamoDeleteType(Key={"finding_id": finding_id})
        resp = await dynamodb_ops.delete_item(TABLE_NAME, delete_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return resp
