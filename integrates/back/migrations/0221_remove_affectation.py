# pylint: disable=invalid-name
"""
This migration wipes event affectation and hours_before_blocking data from
the DB

Affectation:
Execution Time:    2022-05-27 at 17:50:26 UTC-5
Finalization Time: 2022-05-27 at 17:50:41 UTC-5

Hours before blocking:
Execution Time:    2022-06-02 at 14:13:37 UTC-5
Finalization Time: 2022-06-02 at 14:13:58 UTC-5
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
    cast,
)

# Constants
PROD: bool = True

EVENTS_TABLE: str = "fi_events"


async def get_all_events(
    filtering_exp: object = "",
    data_attr: str = "",
) -> list[dict[str, Any]]:
    scan_attrs = {}
    if filtering_exp:
        scan_attrs["FilterExpression"] = filtering_exp
    if data_attr:
        scan_attrs["ProjectionExpression"] = data_attr
    items = await dynamodb_ops.scan(EVENTS_TABLE, scan_attrs)
    return cast(list[dict[str, Any]], items)


async def update(event_id: str, data: dict[str, None]) -> bool:
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
            "event_id": event_id,
        },
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }
    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    if expression_names:
        update_attrs.update({"ExpressionAttributeNames": expression_names})
    try:
        success = await dynamodb_ops.update_item(EVENTS_TABLE, update_attrs)
    except ClientError as ex:
        print(f"- ERROR: {ex}")
    return success


async def process_event(event: dict[str, Any]) -> bool:
    success = False
    if PROD:
        success = await update(
            event["event_id"],
            {"hours_before_blocking": None},
        )
    return success


async def remove_affectations(events: list[dict[str, Any]]) -> None:
    success = all(await collect(process_event(event) for event in events))
    print(f"Hours before blocking removed: {success}")


async def main() -> None:
    events = await get_all_events()
    await remove_affectations(events)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
