# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from .findings import (
    insert_historic_state,
    insert_historic_verification,
    insert_historic_verification_vuln_ids,
    insert_metadata,
    insert_metadata_severity,
)
from dynamodb.types import (
    Item,
    Record,
)


def _process_metadata(item: Item) -> None:
    insert_metadata(item=item)
    insert_metadata_severity(item=item)
    finding_id = item["id"]
    state_items = (
        item.get("state"),
        item.get("creation"),
        item.get("submission"),
        item.get("approval"),
    )
    state_items_filtered = tuple(item for item in state_items if item)
    if state_items_filtered:
        insert_historic_state(
            finding_id=finding_id, historic_state=state_items_filtered
        )
    verification = item.get("verification")
    if verification:
        historic_verification = (verification,)
        insert_historic_verification(
            finding_id=finding_id, historic_verification=historic_verification
        )
        insert_historic_verification_vuln_ids(
            finding_id=finding_id, historic_verification=historic_verification
        )


def process_finding(records: tuple[Record, ...]) -> None:
    metadata_items: list[Item] = [
        record.old_image
        for record in records
        if record.old_image and record.sk.startswith("GROUP#")
    ]
    for item in metadata_items:
        _process_metadata(item)
