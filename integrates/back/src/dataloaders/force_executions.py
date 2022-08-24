from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model.forces.types import (
    ForcesExecution,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from dynamodb.types import (
    Item,
)
from newutils.forces import (
    format_forces,
)
from typing import (
    Iterable,
)

TABLE_NAME = "FI_forces"


async def _get_executions(
    group_name: str,
) -> list[Item]:
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
        result["group_name"] = result.get("subscription")
    return results


class ForcesExecutionsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, forces_keys: Iterable[str]
    ) -> tuple[tuple[ForcesExecution, ...], ...]:
        # Organizations can be loaded either by name or id(preceded by "ORG#")
        list_items = await collect(
            tuple(
                _get_executions(group_name=group_name)
                for group_name in forces_keys
            )
        )
        return tuple(
            tuple(format_forces(item) for item in lists)
            for lists in list_items
        )
