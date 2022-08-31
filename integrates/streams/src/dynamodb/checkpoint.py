from dynamodb.resource import (
    TABLE_RESOURCE,
)
from typing import (
    Optional,
)


def _get_checkpoint_key(shard_id: str) -> dict[str, str]:
    return {"pk": f"SHARD#{shard_id}", "sk": f"SHARD#{shard_id}"}


def get_shard_checkpoint(shard_id: str) -> Optional[str]:
    """Returns the last known iterator for the requested shard"""
    response = TABLE_RESOURCE.get_item(Key=_get_checkpoint_key(shard_id))
    item = response.get("Item")

    if item:
        return item["last_iterator"]

    return None


def remove_shard_checkpoint(shard_id: str) -> None:
    """Removes a checkpoint in the database"""
    TABLE_RESOURCE.delete_item(Key=_get_checkpoint_key(shard_id))


def save_shard_checkpoint(shard_id: str, last_iterator: str) -> None:
    """Saves a checkpoint in the database"""
    TABLE_RESOURCE.put_item(
        Item={
            **_get_checkpoint_key(shard_id),
            "last_iterator": last_iterator,
        }
    )
