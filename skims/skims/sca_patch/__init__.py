# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    run,
)
from custom_exceptions import (
    InvalidActionParameter,
    InvalidPatchItem,
    InvalidPathParameter,
    InvalidScaPatchFormat,
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
from s3.operations import (
    download_advisories,
    upload_advisories,
)
import sys
from typing import (
    Any,
    Dict,
    Iterable,
    List,
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


def remove_from_s3(adv: Advisory, s3_advisories: Dict[str, Any]) -> None:
    if (
        adv.package_manager in s3_advisories
        and adv.package_name in s3_advisories[adv.package_manager]
        and adv.associated_advisory
        in s3_advisories[adv.package_manager][adv.package_name]
    ):
        del s3_advisories[adv.package_manager][adv.package_name][
            adv.associated_advisory
        ]
        if s3_advisories[adv.package_manager][adv.package_name] == {}:
            del s3_advisories[adv.package_manager][adv.package_name]


async def update_s3(to_storage: List[Advisory], action: str) -> None:
    s3_advisories, s3_patch_advisories = await download_advisories()
    if action != REMOVE:
        await upload_advisories(to_storage, s3_advisories, is_patch=True)
    else:
        for adv in to_storage:
            if adv.source == PATCH_SRC:
                remove_from_s3(adv, s3_patch_advisories)
            else:
                remove_from_s3(adv, s3_advisories)
        await upload_advisories(to_storage=[], s3_advisories=s3_advisories)
        await upload_advisories(
            to_storage=[], s3_advisories=s3_patch_advisories
        )


async def patch_sca(filename: str, action: str) -> None:
    with open(filename, "r", encoding="utf-8") as stream:
        try:
            from_json: list = json.load(stream)
            if not isinstance(from_json, list):
                raise InvalidScaPatchFormat()
            items: Advisories = [
                check_item(item, action) for item in from_json
            ]
            for adv in items:
                if action == ADD:
                    await advisories_model.add(advisory=adv, no_overwrite=True)
                elif action == UPDATE:
                    await advisories_model.update(advisory=adv)
                else:
                    await advisories_model.remove(
                        advisory_id=adv.associated_advisory,
                        pkg_name=adv.package_name,
                        platform=adv.package_manager,
                        source=adv.source,
                    )
        except (
            json.JSONDecodeError,
            InvalidPatchItem,
            InvalidScaPatchFormat,
        ) as exc:
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
