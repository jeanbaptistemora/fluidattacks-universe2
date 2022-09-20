# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from .findings import (
    insert_metadata,
    insert_metadata_severity,
)
from dynamodb.types import (
    Record,
)


def process_finding(records: tuple[Record, ...]) -> None:
    metadata_items = [
        record.old_image
        for record in records
        if record.old_image and record.sk.startswith("GROUP#")
    ]
    for item in metadata_items:
        insert_metadata(item=item)
        insert_metadata_severity(item=item)
