# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from . import (
    findings as findings_ops,
)
from .operations import (
    db_cursor,
)
from dynamodb.context import (
    FI_ENVIRONMENT,
)
from dynamodb.types import (
    Item,
    Record,
)
import itertools
from operator import (
    itemgetter,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
)

FLUID_IDENTIFIER = "@fluidattacks.com"


def _process_metadata(cursor: cursor_cls, item: Item) -> None:
    state: Item = item["state"]
    if (
        state["status"] == "DELETED"
        and not str(state["modified_by"]).endswith(FLUID_IDENTIFIER)
        and item.get("approval")
    ):
        findings_ops.insert_finding(cursor=cursor, item=item)
        return

    if state["status"] != "DELETED" or not str(state["modified_by"]).endswith(
        FLUID_IDENTIFIER
    ):
        findings_ops.insert_finding(cursor=cursor, item=item)


def _process_state(
    cursor: cursor_cls, finding_id: str, items: list[Item]
) -> None:
    findings_ops.insert_historic_state(
        cursor=cursor, finding_id=finding_id, historic_state=tuple(items)
    )


def _process_verification(
    cursor: cursor_cls, finding_id: str, items: list[Item]
) -> None:
    findings_ops.insert_historic_verification(
        cursor=cursor,
        finding_id=finding_id,
        historic_verification=tuple(items),
    )
    findings_ops.insert_historic_verification_vuln_ids(
        cursor=cursor,
        finding_id=finding_id,
        historic_verification=tuple(items),
    )


def process_finding(records: tuple[Record, ...]) -> None:
    if FI_ENVIRONMENT != "prod":
        return

    with db_cursor() as cursor:
        metadata_items: list[Item] = [
            record.old_image
            for record in records
            if record.old_image and record.sk.startswith("GROUP#")
        ]
        for item in metadata_items:
            _process_metadata(cursor, item)

        state_items: list[Item] = [
            record.old_image
            for record in records
            if record.old_image and record.sk.startswith("STATE#")
        ]
        state_iterator = itertools.groupby(state_items, itemgetter("pk"))
        for key, items in state_iterator:
            finding_id = str(key).split("#")[1]
            _process_state(cursor, finding_id, list(items))

        verification_items: list[Item] = [
            record.old_image
            for record in records
            if record.old_image and record.sk.startswith("VERIFICATION#")
        ]
        verification_iterator = itertools.groupby(
            verification_items, itemgetter("pk")
        )
        for key, items in verification_iterator:
            finding_id = str(key).split("#")[1]
            _process_verification(cursor, finding_id, list(items))
