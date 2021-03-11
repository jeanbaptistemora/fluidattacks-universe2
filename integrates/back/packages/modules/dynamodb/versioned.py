# Standard
from operator import itemgetter
from typing import Tuple

# Local
from dynamodb.types import Item, PrimaryKey


def get_metadata(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...]
) -> Item:
    return next(
        item
        for item in raw_items
        if item[key_structure.sort_key] == item_id
    )


def get_historic(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    historic_prefix: str,
    raw_items: Tuple[Item, ...]
) -> Tuple[Item, ...]:
    historic_sort_key = f'{item_id}#{historic_prefix}#'
    historic = tuple(
        item
        for item in raw_items
        if item[key_structure.sort_key].startswith(historic_sort_key)
    )

    return tuple(sorted(historic, key=itemgetter(key_structure.sort_key)))
