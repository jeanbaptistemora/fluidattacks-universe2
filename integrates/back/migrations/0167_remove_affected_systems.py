# pylint: disable=invalid-name
"""
This migration wipes affected systems data from the findings DB

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from aiohttp.client_exceptions import (
    ClientError,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import time
from typing import (
    Any,
    Dict,
    List,
)

# Constants
PROD: bool = True

FINDINGS_TABLE: str = "integrates_vms"


async def get_all_findings(
    filtering_exp: object = "",
    data_attr: str = "",
) -> List[Dict[str, Any]]:
    scan_attrs = {}
    if filtering_exp:
        scan_attrs["FilterExpression"] = filtering_exp
    if data_attr:
        scan_attrs["ProjectionExpression"] = data_attr
    items = await dynamodb_ops.scan(FINDINGS_TABLE, scan_attrs)
    return items


async def update(pk: str, sk: str, data: Dict[str, None]) -> bool:
    """Manually updates db data"""
    success = False
    set_expression = ""
    remove_expression = ""
    expression_names = {}
    expression_values = {}  # type: ignore
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
            "pk": pk,
            "sk": sk,
        },
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }
    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    if expression_names:
        update_attrs.update({"ExpressionAttributeNames": expression_names})
    try:
        success = await dynamodb_ops.update_item(FINDINGS_TABLE, update_attrs)
    except ClientError as ex:
        print(f"- ERROR: {ex}")
    return success


async def process_finding(finding: Dict[str, Any]) -> bool:
    success = False
    if PROD and "affected_systems" in finding:
        success = await update(
            finding["pk"],
            finding["sk"],
            {"affected_systems": None},
        )
        print(f"Removed affected_systems from: {finding['pk']}")
    return success


async def remove_affected_systems(findings: List[Dict[str, Any]]) -> None:
    success = all(
        await collect(process_finding(finding) for finding in findings)
    )
    print(f"Affected systems removed: {success}")


async def main() -> None:
    findings = await get_all_findings()
    await remove_affected_systems(findings[0:1])


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
