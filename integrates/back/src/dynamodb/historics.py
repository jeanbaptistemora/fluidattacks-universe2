from dynamodb import (
    keys,
)
from dynamodb.types import (
    Facet,
    Item,
    PrimaryKey,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    Dict,
    Optional,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def get_metadata(
    *, item_id: str, key_structure: PrimaryKey, raw_items: Tuple[Item, ...]
) -> Item:
    return next(
        item for item in raw_items if item[key_structure.sort_key] == item_id
    )


def get_latest(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    historic_suffix: str,
    raw_items: Tuple[Item, ...],
) -> Item:
    historic_sort_key = f"{item_id}#{historic_suffix}"
    try:
        return next(
            item
            for item in raw_items
            if item[key_structure.sort_key] == historic_sort_key
        )
    except StopIteration:
        LOGGER.error(
            "Couldn't get the historic status", extra={"extra": locals()}
        )

        raise


def get_optional_latest(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    historic_suffix: str,
    raw_items: Tuple[Item, ...],
) -> Optional[Item]:
    try:
        latest: Optional[Item] = get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix=historic_suffix,
            raw_items=raw_items,
        )
    except StopIteration:
        latest = None

    return latest


def build_historic(
    *,
    attributes: Item,
    historic_facet: Facet,
    key_structure: PrimaryKey,
    key_values: Dict[str, str],
    latest_facet: Facet,
) -> Tuple[Item, Item]:
    latest_key = keys.build_key(facet=latest_facet, values=key_values)
    latest = {
        key_structure.partition_key: latest_key.partition_key,
        key_structure.sort_key: latest_key.sort_key,
        **attributes,
    }

    historic_key = keys.build_key(facet=historic_facet, values=key_values)
    historic = {
        key_structure.partition_key: historic_key.partition_key,
        key_structure.sort_key: historic_key.sort_key,
        **attributes,
    }

    return (latest, historic)
