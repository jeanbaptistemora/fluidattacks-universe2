from aioextensions import (
    run,
)
from custom_exceptions import (
    InvalidActionParameter,
    InvalidPatchItem,
    InvalidPathParameter,
)
from db_model import (
    advisories as advisories_model,
)
from db_model.advisories.constants import (
    PATCH_SRC,
)
from db_model.advisories.types import (
    Advisory,
)
from dynamodb.resource import (
    dynamo_shutdown,
    dynamo_startup,
)
import json
import sys
from typing import (
    Iterable,
)
from utils.logs import (
    log_blocking,
)

Advisories = Iterable[Advisory]
ADD = "add"
REMOVE = "remove"
UPDATE = "update"


def check_item(item: dict, action: str) -> Advisory:
    if not all(
        key in item
        for key in (
            "package_name",
            "package_manager",
            "associated_advisory",
        )
    ) or (action == REMOVE and "source" not in item):
        raise InvalidPatchItem()
    if action != REMOVE and not all(
        key in item for key in ("vulnerable_version", "severity")
    ):
        raise InvalidPatchItem()

    return Advisory(
        associated_advisory=item["associated_advisory"],
        package_manager=item["package_manager"],
        package_name=item["package_name"],
        source=item["source"] if action == REMOVE else PATCH_SRC,
        vulnerable_version=item.get("vulnerable_version", ""),
        severity=item.get("severity"),
    )


async def patch_sca(filename: str, action: str) -> None:
    with open(filename, "r", encoding="utf-8") as stream:
        try:
            from_json: list = json.load(stream)
            items: Advisories = [
                check_item(item, action)
                for item in (from_json if isinstance(from_json, list) else [])
            ]
            for adv in items:
                if action == ADD:
                    await advisories_model.add(advisory=adv)
                elif action == UPDATE:
                    await advisories_model.update(advisory=adv)
                else:
                    await advisories_model.remove(
                        advisory_id=adv.associated_advisory,
                        pkg_name=adv.package_name,
                        platform=adv.package_manager,
                        source=adv.source,
                    )
        except (json.JSONDecodeError, InvalidPatchItem) as exc:
            log_blocking("error", "%s", exc.msg)


async def main() -> None:
    try:
        action = sys.argv[1]
        if action not in (ADD, UPDATE, REMOVE):
            raise InvalidActionParameter()
        path = sys.argv[2]
        if not path:
            raise InvalidPathParameter()

        await dynamo_startup()
        await patch_sca(path, action)
    except (InvalidActionParameter, InvalidPathParameter) as exc:
        log_blocking("error", "%s", exc.msg)
    finally:
        await dynamo_shutdown()


if __name__ == "__main__":
    run(main())
