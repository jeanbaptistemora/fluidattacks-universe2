# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dynamodb.resource import (
    TABLE_RESOURCE,
)
from typing import (
    Optional,
)


def _get_checkpoint_key(shard_id: str) -> dict[str, str]:
    """Returns the primary key for the requested shard"""
    return {"pk": f"SHARD#{shard_id}", "sk": f"SHARD#{shard_id}"}


def get_checkpoint(shard_id: str) -> Optional[str]:
    """Returns the last known sequence number for the requested shard"""
    response = TABLE_RESOURCE.get_item(Key=_get_checkpoint_key(shard_id))
    item = response.get("Item")

    if item:
        return item["last_sequence_number"]

    return None


def remove_checkpoint(shard_id: str) -> None:
    """Removes a checkpoint in the database"""
    TABLE_RESOURCE.delete_item(Key=_get_checkpoint_key(shard_id))


def save_checkpoint(shard_id: str, last_sequence_number: str) -> None:
    """Saves a checkpoint in the database"""
    TABLE_RESOURCE.put_item(
        Item={
            **_get_checkpoint_key(shard_id),
            "last_sequence_number": last_sequence_number,
        }
    )
