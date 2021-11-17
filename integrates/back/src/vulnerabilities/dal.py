import aioboto3
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_S3_REPORTS_BUCKET as VULNS_BUCKET,
)
from custom_exceptions import (
    VulnNotFound,
)
from custom_types import (
    DynamoDelete as DynamoDeleteType,
    Finding as FindingType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
from newutils.vulnerabilities import (
    format_vulnerability_item,
    format_vulnerability_treatment_item,
)
from s3 import (
    operations as s3_ops,
)
from settings import (
    LOGGING,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "FI_vulnerabilities"


async def create(data: Dict[str, FindingType]) -> bool:
    """Add vulnerabilities."""
    resp = False
    try:
        item = {
            "finding_id": str(data.get("finding_id")),
            "UUID": str(data.get("UUID")),
            "vuln_type": data.get("vuln_type"),
            "where": data.get("where"),
            "source": str(data.get("source", "asm")),
            "specific": str(data.get("specific")),
            "historic_treatment": data.get("historic_treatment"),
            "historic_state": data.get("historic_state"),
        }
        if "stream" in data:
            item["stream"] = data["stream"]
        if "commit_hash" in data:
            item["commit_hash"] = data["commit_hash"]
        if "historic_verification" in data:
            item["historic_verification"] = data["historic_verification"]
        if data.get("repo_nickname"):
            item["repo_nickname"] = data["repo_nickname"]
        resp = await dynamodb_ops.put_item(TABLE_NAME, item)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return resp


async def create_new(
    vulnerability: Vulnerability,
    historic_treatment: Optional[Tuple[VulnerabilityTreatment, ...]] = None,
) -> bool:
    """Add vulnerability."""
    item = format_vulnerability_item(vulnerability)
    if historic_treatment:
        item["historic_treatment"] = [
            format_vulnerability_treatment_item(treatment)
            for treatment in historic_treatment
        ]
    try:
        return await dynamodb_ops.put_item(TABLE_NAME, item)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return False


async def delete(uuid: str, finding_id: str) -> bool:
    """Delete a vulnerability of a finding."""
    resp = False
    try:
        delete_attrs = DynamoDeleteType(
            Key={"UUID": uuid, "finding_id": finding_id}
        )
        resp = await dynamodb_ops.delete_item(TABLE_NAME, delete_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return resp


async def get(vuln_uuid: str) -> List[Dict[str, FindingType]]:
    """Get a vulnerability by only its UUID."""
    hash_key = "UUID"
    query_attrs = {
        "IndexName": "gsi_uuid",
        "KeyConditionExpression": Key(hash_key).eq(vuln_uuid),
    }
    return await dynamodb_ops.query(TABLE_NAME, query_attrs)


async def get_by_finding(
    finding_id: str,
    vuln_type: str = "",
    where: str = "",
    specific: str = "",
    uuid: str = "",
) -> List[Dict[str, FindingType]]:
    """Get a vulnerability."""
    hash_key = "finding_id"
    query_attrs = {"KeyConditionExpression": Key(hash_key).eq(finding_id)}
    if finding_id and uuid:
        range_key = "UUID"
        query_attrs.update(
            {
                "KeyConditionExpression": (
                    Key(hash_key).eq(finding_id) & Key(range_key).eq(uuid)
                )
            }
        )
    elif finding_id and vuln_type and where and specific:
        filtering_exp = (
            Attr("vuln_type").eq(vuln_type)
            & Attr("where").eq(where)
            & Attr("specific").eq(specific)
        )
        query_attrs.update({"FilterExpression": filtering_exp})
    return await dynamodb_ops.query(TABLE_NAME, query_attrs)


async def get_vulnerabilities_async(
    finding_id: str,
    table: aioboto3.session.Session.client,
    should_list_deleted: bool = False,
) -> List[Dict[str, FindingType]]:
    """Get vulnerabilities of the given finding"""
    query_attrs = {"KeyConditionExpression": Key("finding_id").eq(finding_id)}
    response = await table.query(**query_attrs)
    vulns = response.get("Items", [])
    while "LastEvaluatedKey" in response:
        query_attrs.update(
            {"ExclusiveStartKey": response.get("LastEvaluatedKey")}
        )
        response = await table.query(**query_attrs)
        vulns += response.get("Items", [])
    return [
        vuln
        for vuln in vulns
        if (
            vuln.get("historic_state", [{}])[-1].get("state") != "DELETED"
            or should_list_deleted
        )
    ]


async def get_vulnerability_by_id(
    vulnerability_uuid: str,
    table: aioboto3.session.Session.client,
) -> List[Dict[str, FindingType]]:
    hash_key = "UUID"
    query_attrs = {
        "IndexName": "gsi_uuid",
        "KeyConditionExpression": Key(hash_key).eq(vulnerability_uuid),
    }
    response = await table.query(**query_attrs)
    vulnerabilities = response.get("Items", [])
    while "LastEvaluatedKey" in response:
        query_attrs.update(
            {"ExclusiveStartKey": response.get("LastEvaluatedKey")}
        )
        response = await table.query(**query_attrs)
        vulnerabilities += response.get("Items", [])

    if not vulnerabilities:
        raise VulnNotFound()
    first_vuln = cast(Dict[str, List[Dict[str, str]]], vulnerabilities[0])
    if (
        first_vuln.get("historic_state", [{}])[-1].get("state", "")
        == "DELETED"
    ):
        raise VulnNotFound()

    return [vulnerabilities[0]]


async def sign_url(vuln_file_name: str) -> str:
    return await s3_ops.sign_url(vuln_file_name, 10, VULNS_BUCKET)


async def update(
    finding_id: str, vuln_id: str, data: Dict[str, FindingType]
) -> bool:
    success = False
    set_expression = ""
    remove_expression = ""
    expression_names = {}
    expression_values = {}
    for attr, value in data.items():
        if value is None:
            remove_expression += f"#{attr}, "
            expression_names.update({f"#{attr}": attr})
        else:
            set_expression += f"#{attr} = :{attr}, "
            expression_names.update({f"#{attr}": attr})
            expression_values.update({f":{attr}": value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'

    update_attrs = {
        "Key": {
            "finding_id": finding_id,
            "UUID": vuln_id,
        },
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }
    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    if expression_names:
        update_attrs.update({"ExpressionAttributeNames": expression_names})
    try:
        success = await dynamodb_ops.update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def append(
    *,
    finding_id: str,
    vulnerability_id: str,
    elements: Dict[str, Tuple[Dict[str, Any], ...]],
) -> None:
    expression = ",".join(
        (f"#{attr} = list_append(#{attr}, :{attr})" for attr in elements)
    )
    expression_names = {f"#{attr}": attr for attr in elements}
    expression_values = {
        f":{attr}": list(values) for attr, values in elements.items()
    }
    await dynamodb_ops.update_item(
        TABLE_NAME,
        {
            "Key": {"finding_id": finding_id, "UUID": vulnerability_id},
            "UpdateExpression": f"SET {expression}",
            "ExpressionAttributeNames": expression_names,
            "ExpressionAttributeValues": expression_values,
        },
    )


async def upload_file(vuln_file: UploadFile) -> str:
    file_path = vuln_file.filename
    file_name = file_path.split("/")[-1]
    await s3_ops.upload_memory_file(
        VULNS_BUCKET,
        vuln_file,
        file_name,
    )
    return cast(str, file_name)
