from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_S3_REPORTS_BUCKET as VULNS_BUCKET,
)
from custom_exceptions import (
    UnavailabilityError,
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
import logging.config
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
    Optional,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "FI_vulnerabilities"


async def add(vulnerability: Vulnerability) -> None:
    """Add vulnerability."""
    await vulns_model.add(vulnerability=vulnerability)


async def sign_url(vuln_file_name: str) -> str:
    return await s3_ops.sign_url(vuln_file_name, 10, VULNS_BUCKET)


async def update(finding_id: str, vuln_id: str, data: Dict[str, Any]) -> bool:
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


async def append(
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
    if not deleted:
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
    await vulns_model.update_historic_entry(
        current_entry=current_value,
        entry=treatment,
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
    )
    await vulns_model.update_assigned_index(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        entry=treatment,
    )


async def update_historic_treatment(
    *,
    finding_id: str,
    vulnerability_id: str,
    historic_treatment: Tuple[VulnerabilityTreatment, ...],
    deleted: Optional[bool] = False,
) -> None:
    if not deleted:
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
    await vulns_model.update_historic(
        finding_id=finding_id,
        historic=historic_zero_risk,
        vulnerability_id=vulnerability_id,
    )
