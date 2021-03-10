# Standard library
from collections import defaultdict
from typing import (
    Dict,
    Optional,
    Set,
    Tuple
)

# Third party
from boto3.dynamodb.conditions import Key

# Local
from dynamodb import operations, versioned
from dynamodb.table import TABLE
from dynamodb.types import (
    Entity,
    Item,
    PrimaryKey,
    RootHistoricCloning,
    RootHistoricState,
    RootItem,
    RootMetadata
)


# Constants
RESERVED_WORDS: Set[str] = {
    '#',
}

ENTITIES: Dict[str, Entity] = dict(
    ROOT=Entity(
        primary_key=PrimaryKey(
            partition_key='GROUP#',
            sort_key='ROOT#',
        ),
    ),
)


def validate_pkey_not_empty(*, key: str) -> None:
    if not key:
        raise ValueError('Partition key cannot be empty')


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


def build_key(
    *,
    entity: str,
    partition_key: str,
    sort_key: Tuple[str, ...]
) -> PrimaryKey:
    validate_entity(entity=entity)
    validate_pkey_not_empty(key=partition_key)
    for key in {partition_key, *sort_key}:
        validate_key_type(key=key)
        validate_key_words(key=key)

    prefix = ENTITIES[entity].primary_key
    composite_pkey: str = f'{prefix.partition_key}{partition_key}'
    composite_skey: str = f'{prefix.sort_key}{"#".join(sort_key)}'

    # >>> build_key(entity='ROOT', partition_key='group-1', sort_key='root-1')
    # PrimaryKey(partition_key='GROUP#group-1', sort_key='ROOT#root-1')
    # >>> build_key(entity='ROOT', partition_key='group-1', sort_key='')
    # PrimaryKey(partition_key='GROUP#group-1', sort_key='')
    return PrimaryKey(
        partition_key=composite_pkey,
        sort_key=composite_skey,
    )


def build_root(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> RootItem:
    historic_cloning = versioned.get_historic(
        item_id=item_id,
        key_structure=key_structure,
        historic_prefix='CLON',
        raw_items=raw_items
    )
    historic_state = versioned.get_historic(
        item_id=item_id,
        key_structure=key_structure,
        historic_prefix='HIST',
        raw_items=raw_items
    )
    metadata = versioned.get_metadata(
        item_id=item_id,
        key_structure=key_structure,
        raw_items=raw_items
    )

    return RootItem(
        historic_cloning=tuple(
            RootHistoricCloning(
                modified_date=item['modified_date'],
                reason=item['reason'],
                status=item['status']
            )
            for item in historic_cloning
        ),
        historic_state=tuple(
            RootHistoricState(
                environment_urls=item['environment_urls'],
                environment=item['environment'],
                gitignore=item['gitignore'],
                includes_health_check=item['includes_health_check'],
                modified_by=item['modified_by'],
                modified_date=item['modified_date'],
                status=item['status']
            )
            for item in historic_state
        ),
        metadata=RootMetadata(
            branch=metadata['branch'],
            type=metadata['type'],
            url=metadata['url']
        )
    )


async def get_root(
    *,
    group_name: str,
    url: str,
    branch: str
) -> Optional[RootItem]:
    primary_key = build_key(
        entity='ROOT',
        partition_key=group_name,
        sort_key=(url, branch)
    )

    index = TABLE.indexes['inverted_index']
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key) &
            Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(
            TABLE.facets['root_metadata'],
            TABLE.facets['root_historic'],
            TABLE.facets['root_cloning_historic']
        ),
        index=index,
        table=TABLE
    )

    if results:
        return build_root(
            item_id=primary_key.sort_key,
            key_structure=key_structure,
            raw_items=results
        )

    return None


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    primary_key = build_key(
        entity='ROOT',
        partition_key=group_name,
        sort_key=()
    )

    index = TABLE.indexes['inverted_index']
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key) &
            Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(
            TABLE.facets['root_metadata'],
            TABLE.facets['root_historic'],
            TABLE.facets['root_cloning_historic']
        ),
        index=index,
        table=TABLE
    )

    root_items = defaultdict(lambda: [])
    for item in results:
        root_id = '#'.join(item[key_structure.sort_key].split('#')[:3])
        root_items[root_id].append(item)

    return tuple(
        build_root(
            item_id=root_id,
            key_structure=key_structure,
            raw_items=tuple(items)
        )
        for root_id, items in root_items.items()
    )
