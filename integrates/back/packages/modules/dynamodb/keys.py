# Standard
from functools import reduce
from typing import Dict, Set

# Local
from dynamodb.types import Facet, PrimaryKey


# Constants
RESERVED_WORDS: Set[str] = {
    '#',
}


def _validate_key_words(*, key: str) -> None:
    for word in RESERVED_WORDS:
        if word in key:
            raise ValueError(
                f'Invalid key, got: {key} with invalid word: "{word}"'
            )


def _build_composite_key(*, template: str, values: Dict[str, str]) -> str:
    key_parts = tuple(part for part in template.split('#'))

    return reduce(
        lambda current, part: (
            current +
            (
                f'{values[part]}#'
                if part in values
                else str()
            ) if part.islower() else f'{part}#'
        ),
        key_parts,
        str()
    )


def build_key(*, facet: Facet, values: Dict[str, str]) -> PrimaryKey:
    for key in values:
        _validate_key_words(key=key)

    composite_pk: str = _build_composite_key(
        template=facet.pk_alias,
        values=values
    )
    composite_sk: str = _build_composite_key(
        template=facet.sk_alias,
        values=values
    )

    return PrimaryKey(
        partition_key=composite_pk,
        sort_key=composite_sk,
    )
