from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from db_model.forces.types import (
    ForcesExecution,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from newutils.forces import (
    format_forces,
)
from typing import (
    Any,
    Iterable,
)

TABLE_NAME = "FI_forces"


async def _get_execution(group_name: str, execution_id: str) -> Any:
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


class OrganizationLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, forces_keys: Iterable[tuple[str, str]]
    ) -> tuple[ForcesExecution, ...]:
        # Organizations can be loaded either by name or id(preceded by "ORG#")
        items = await collect(
            tuple(
                _get_execution(
                    group_name=group_name, execution_id=execution_id
                )
                for group_name, execution_id in forces_keys
            )
        )
        return tuple(format_forces(item) for item in items)
