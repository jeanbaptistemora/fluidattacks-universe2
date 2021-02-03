# Standard library

from typing import (
    Dict,
    NamedTuple,
    Set,
    Any,
)


class PrimaryKey(NamedTuple):
    pkey: str
    skey: str


class Entity(NamedTuple):
    primary_key: PrimaryKey
    attrs: Set[Any]
    dependencies: Set[Any]


# Constants

RESERVED_WORDS: Set[str] = {
    '#',
    '/',
}


ENTITIES: Dict[str, Entity] = dict(
    ROOT=Entity(
        primary_key=PrimaryKey(
            pkey='GROUP#',
            skey='ROOT#',
        ),
        attrs={
            'branch',
            'kind',
            'url',
            'environment_urls',
        },
        dependencies=set(),
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


def build_key(*, entity: str, pkey: str, skey: str) -> PrimaryKey:
    validate_entity(entity=entity)
    validate_pkey_not_empty(key=pkey)
    for key in [pkey, skey]:
        validate_key_type(key=key)
        validate_key_words(key=key)

    composite_pkey: str = f'{ENTITIES[entity].primary_key.pkey}{pkey}'
    composite_skey: str = ''
    if skey:
        composite_skey = f'{ENTITIES[entity].primary_key.skey}{skey}'

    # >>> build_key(entity='ROOT', pkey='group-1', skey='root-1')
    # PrimaryKey(pkey='GROUP#group-1', skey='ROOT#root-1')
    # >>> build_key(entity='ROOT', pkey='group-1', skey='')
    # PrimaryKey(pkey='GROUP#group-1', skey='')
    return PrimaryKey(
        pkey=composite_pkey,
        skey=composite_skey,
    )
