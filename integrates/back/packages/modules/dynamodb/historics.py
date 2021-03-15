# Standard
from typing import Dict, Tuple

# Local
from dynamodb import keys
from dynamodb.types import Facet, Item, PrimaryKey


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


def get_latest(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    historic_prefix: str,
    raw_items: Tuple[Item, ...]
) -> Item:
    historic_sort_key = f'{item_id}#{historic_prefix}'

    return next(
        item
        for item in raw_items
        if item[key_structure.sort_key] == historic_sort_key
    )


def build_historic(
    *,
    attributes: Item,
    historic_facet: Facet,
    key_structure: PrimaryKey,
    key_values: Dict[str, str],
    latest_facet: Facet
) -> Tuple[Item, Item]:
    latest_key = keys.build_key(facet=latest_facet, values=key_values)
    latest = {
        key_structure.partition_key: latest_key.partition_key,
        key_structure.sort_key: latest_key.sort_key,
        **attributes
    }

    historic_key = keys.build_key(facet=historic_facet, values=key_values)
    historic = {
        key_structure.partition_key: historic_key.partition_key,
        key_structure.sort_key: historic_key.sort_key,
        **attributes
    }

    return (latest, historic)
