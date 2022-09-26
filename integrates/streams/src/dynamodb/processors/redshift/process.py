# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from . import (
    findings as findings_ops,
)
from dynamodb.types import (
    Item,
    Record,
)

FLUID_IDENTIFIER = "@fluidattacks.com"


def _process_metadata(item: Item) -> None:
    state: Item = item["state"]
    if (
        state["status"] == "DELETED"
        and not str(state["modified_by"]).endswith(FLUID_IDENTIFIER)
        and item.get("approval")
    ):
        findings_ops.insert_finding(item=item)
        return

    if state["status"] != "DELETED" or not str(state["modified_by"]).endswith(
        FLUID_IDENTIFIER
    ):
        findings_ops.insert_finding(item=item)


def process_finding(records: tuple[Record, ...]) -> None:
    metadata_items: list[Item] = [
        record.old_image
        for record in records
        if record.old_image and record.sk.startswith("GROUP#")
    ]
    for item in metadata_items:
        _process_metadata(item=item)
