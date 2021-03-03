# Standard library
from typing import (
    Dict,
    NamedTuple,
    Set,
)


class PrimaryKey(NamedTuple):
    partition_key: str
    sort_key: str


class Entity(NamedTuple):
    primary_key: PrimaryKey
    attrs: Set[str]


# Constants
RESERVED_WORDS: Set[str] = {
    '#',
    '/',
}


ENTITIES: Dict[str, Entity] = dict(
    ROOT=Entity(
        primary_key=PrimaryKey(
            partition_key='GROUP#',
            sort_key='ROOT#',
        ),
        attrs={
            'branch',
            'kind',
            'url',
            'environment_urls',
        },
    ),
)


def validate_pkey_not_empty(*, key: str) -> None:
    if not key:
        raise ValueError(f'Partition key cannot be empty')


def validate_entity(*, entity: str) -> None:
    if entity not in ENTITIES:
        raise ValueError(f'Invalid entity: {entity}')


def validate_key_type(*, key: str) -> None:
    if not isinstance(key, str):
        raise TypeError(f'Expected str, got: {type(key)}')


def validate_key_words(*, key: str) -> None:
    for word in RESERVED_WORDS:
        if word in key:
            raise ValueError(
                f'Invalid key, got: {key} with invalid word: "{word}"'
            )


def build_key(*, entity: str, partition_key: str, sort_key: str) -> PrimaryKey:
    validate_entity(entity=entity)
    validate_pkey_not_empty(key=partition_key)
    for key in [partition_key, sort_key]:
        validate_key_type(key=key)
        validate_key_words(key=key)

    prefix = ENTITIES[entity].primary_key
    composite_pkey: str = f'{prefix.partition_key}{partition_key}'
    composite_skey: str = (
        f'{prefix.sort_key}{sort_key}'
        if sort_key
        else prefix.sort_key
    )

    # >>> build_key(entity='ROOT', partition_key='group-1', sort_key='root-1')
    # PrimaryKey(partition_key='GROUP#group-1', sort_key='ROOT#root-1')
    # >>> build_key(entity='ROOT', partition_key='group-1', sort_key='')
    # PrimaryKey(partition_key='GROUP#group-1', sort_key='')
    return PrimaryKey(
        partition_key=composite_pkey,
        sort_key=composite_skey,
    )
