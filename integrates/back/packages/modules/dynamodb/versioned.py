# Standard
from operator import itemgetter
from typing import List, Tuple

# Local
from dynamodb.types import Item, PrimaryKey


def get_metadata(
    *,
    primary_key: PrimaryKey,
    raw_items: List[Item]
) -> Item:
    return next(
        item
        for item in raw_items
        if item['sk'] == primary_key.sort_key
    )


def get_historic(
    *,
    primary_key: PrimaryKey,
    historic_prefix: str,
    raw_items: List[Item]
) -> Tuple[Item, ...]:
    historic_sort_key = f'{primary_key.sort_key}#{historic_prefix}#'
    historic = tuple(
        item
        for item in raw_items
        if item['sk'].startswith(historic_sort_key)
    )

    return tuple(sorted(historic, key=itemgetter('sk'), reverse=True))
