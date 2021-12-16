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
    FI_ENVIRONMENT,
)
from custom_exceptions import (
    UnavailabilityError,
    VulnNotFound,
)
import db_model.vulnerabilities as vulns_model
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
from newutils.vulnerabilities import (
    format_vulnerability_item,
    format_vulnerability_metadata_item,
    format_vulnerability_state_item,
    format_vulnerability_treatment_item,
    format_vulnerability_verification_item,
    format_vulnerability_zero_risk_item,
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
    Dict,
    List,
    Optional,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "FI_vulnerabilities"


async def add(vulnerability: Vulnerability) -> None:
    """Add vulnerability."""
    item = format_vulnerability_item(vulnerability)

    try:
        await dynamodb_ops.put_item(TABLE_NAME, item)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
        raise UnavailabilityError() from ex

    if (
        FI_ENVIRONMENT == "development"
        and vulnerability.state.status != VulnerabilityStateStatus.DELETED
    ):
        await vulns_model.add(vulnerability=vulnerability)


async def get_by_finding(
    finding_id: str,
    vuln_type: str = "",
    where: str = "",
    specific: str = "",
    uuid: str = "",
) -> List[Dict[str, Any]]:
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


async def get_vulnerability_by_id(
    vulnerability_uuid: str,
    table: aioboto3.session.Session.client,
) -> List[Dict[str, Any]]:
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
    first_vuln = vulnerabilities[0]
    if (
        first_vuln.get("historic_state", [{}])[-1].get("state", "")
        == "DELETED"
    ):
        raise VulnNotFound()

    return [vulnerabilities[0]]


async def sign_url(vuln_file_name: str) -> str:
    return await s3_ops.sign_url(vuln_file_name, 10, VULNS_BUCKET)


async def _update(finding_id: str, vuln_id: str, data: Dict[str, Any]) -> bool:
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
        return await dynamodb_ops.update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
        raise UnavailabilityError() from ex


async def _append(
    *,
    finding_id: str,
    vulnerability_id: str,
    elements: Dict[str, Tuple[Dict[str, Any], ...]],
) -> None:
    expression = ",".join(
        (
            f"#{attr} = list_append(if_not_exists(#{attr}, :_empty), :{attr})"
            for attr in elements
        )
    )
    expression_names = {f"#{attr}": attr for attr in elements}
    utility_values: Dict[str, list] = {":_empty": []}
    expression_values = {
        f":{attr}": list(values) for attr, values in elements.items()
    }
    await dynamodb_ops.update_item(
        TABLE_NAME,
        {
            "Key": {"finding_id": finding_id, "UUID": vulnerability_id},
            "UpdateExpression": f"SET {expression}",
            "ExpressionAttributeNames": expression_names,
            "ExpressionAttributeValues": {
                **utility_values,
                **expression_values,
            },
        },
    )


async def upload_file(vuln_file: UploadFile) -> str:
    file_path: str = vuln_file.filename
    file_name: str = file_path.split("/")[-1]
    await s3_ops.upload_memory_file(
        VULNS_BUCKET,
        vuln_file,
        file_name,
    )
    return file_name


async def update_metadata(
    *,
    finding_id: str,
    vulnerability_id: str,
    metadata: VulnerabilityMetadataToUpdate,
    deleted: Optional[bool] = False,
) -> None:
    item = format_vulnerability_metadata_item(metadata)
    if item:
        await _update(
            finding_id=finding_id,
            vuln_id=vulnerability_id,
            data=item,
        )
    if FI_ENVIRONMENT == "development" and not deleted:
        await vulns_model.update_metadata(
            finding_id=finding_id,
            metadata=metadata,
            vulnerability_id=vulnerability_id,
        )


async def update_state(
    *,
    current_value: VulnerabilityState,
    finding_id: str,
    vulnerability_id: str,
    state: VulnerabilityState,
) -> None:
    item = format_vulnerability_state_item(state)
    await _append(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        elements={"historic_state": (item,)},
    )
    if FI_ENVIRONMENT == "development":
        if state.status == VulnerabilityStateStatus.DELETED:
            # Keep deleted items out of the new model while we define the path
            # going forward for archived data
            # details at https://gitlab.com/fluidattacks/product/-/issues/5690
            await vulns_model.remove(vulnerability_id=vulnerability_id)
        else:
            await vulns_model.update_historic_entry(
                current_entry=current_value,
                entry=state,
                finding_id=finding_id,
                vulnerability_id=vulnerability_id,
            )


async def update_historic_state(
    *,
    finding_id: str,
    vulnerability_id: str,
    historic_state: Tuple[VulnerabilityState, ...],
) -> None:
    await _update(
        finding_id=finding_id,
        vuln_id=vulnerability_id,
        data={
            "historic_state": [
                format_vulnerability_state_item(state)
                for state in historic_state
            ]
        },
    )
    if FI_ENVIRONMENT == "development":
        await vulns_model.update_historic(
            finding_id=finding_id,
            historic=historic_state,
            vulnerability_id=vulnerability_id,
        )


async def update_treatment(
    *,
    current_value: Optional[VulnerabilityTreatment],
    finding_id: str,
    vulnerability_id: str,
    treatment: VulnerabilityTreatment,
) -> None:
    item = format_vulnerability_treatment_item(treatment)
    await _append(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        elements={"historic_treatment": (item,)},
    )
    if FI_ENVIRONMENT == "development":
        await vulns_model.update_historic_entry(
            current_entry=current_value,
            entry=treatment,
            finding_id=finding_id,
            vulnerability_id=vulnerability_id,
        )


async def update_historic_treatment(
    *,
    finding_id: str,
    vulnerability_id: str,
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
    deleted: Optional[bool] = False,
) -> None:
    await _update(
        finding_id=finding_id,
        vuln_id=vulnerability_id,
        data={
            "historic_treatment": [
                format_vulnerability_treatment_item(treatment)
                for treatment in historic_treatment
            ]
        },
    )
    if FI_ENVIRONMENT == "development" and not deleted:
        await vulns_model.update_historic(
            finding_id=finding_id,
            historic=historic_treatment,
            vulnerability_id=vulnerability_id,
        )


async def update_verification(
    *,
    current_value: Optional[VulnerabilityVerification],
    finding_id: str,
    vulnerability_id: str,
    verification: VulnerabilityVerification,
) -> None:
    item = format_vulnerability_verification_item(verification)
    await _append(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        elements={"historic_verification": (item,)},
    )
    if FI_ENVIRONMENT == "development":
        await vulns_model.update_historic_entry(
            current_entry=current_value,
            entry=verification,
            finding_id=finding_id,
            vulnerability_id=vulnerability_id,
        )


async def update_historic_verification(
    *,
    finding_id: str,
    vulnerability_id: str,
    historic_verification: Tuple[VulnerabilityVerification, ...],
) -> None:
    await _update(
        finding_id=finding_id,
        vuln_id=vulnerability_id,
        data={
            "historic_verification": [
                format_vulnerability_verification_item(verification)
                for verification in historic_verification
            ]
        },
    )
    if FI_ENVIRONMENT == "development":
        await vulns_model.update_historic(
            finding_id=finding_id,
            historic=historic_verification,
            vulnerability_id=vulnerability_id,
        )


async def update_zero_risk(
    *,
    current_value: Optional[VulnerabilityZeroRisk],
    finding_id: str,
    vulnerability_id: str,
    zero_risk: VulnerabilityZeroRisk,
) -> None:
    item = format_vulnerability_zero_risk_item(zero_risk)
    await _append(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        elements={"historic_zero_risk": (item,)},
    )
    if FI_ENVIRONMENT == "development":
        await vulns_model.update_historic_entry(
            current_entry=current_value,
            entry=zero_risk,
            finding_id=finding_id,
            vulnerability_id=vulnerability_id,
        )


async def update_historic_zero_risk(
    *,
    finding_id: str,
    vulnerability_id: str,
    historic_zero_risk: Tuple[VulnerabilityZeroRisk, ...],
) -> None:
    await _update(
        finding_id=finding_id,
        vuln_id=vulnerability_id,
        data={
            "historic_zero_risk": [
                format_vulnerability_zero_risk_item(zero_risk)
                for zero_risk in historic_zero_risk
            ]
        },
    )
    if FI_ENVIRONMENT == "development":
        await vulns_model.update_historic(
            finding_id=finding_id,
            historic=historic_zero_risk,
            vulnerability_id=vulnerability_id,
        )
