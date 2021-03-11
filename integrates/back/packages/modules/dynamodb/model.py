# Standard library
from collections import defaultdict
from functools import reduce
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
    Facet,
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


def _validate_key_words(*, key: str) -> None:
    for word in RESERVED_WORDS:
        if word in key:
            raise ValueError(
                f'Invalid key, got: {key} with invalid word: "{word}"'
            )


def _build_composite_key(*, template: str, values: Dict[str, str]) -> str:
    if values:
        key_parts = tuple(
            part
            for part in template.split('#')
            if part.islower()
        )

        return reduce(
            lambda current, part: current.replace(part, values[part]),
            key_parts,
            template
        )

    return f'{template.split("#")[0]}#'


def _build_key(
    *,
    facet: Facet,
    pk_values: Dict[str, str],
    sk_values: Dict[str, str]
) -> PrimaryKey:
    for key in {*pk_values.values(), *sk_values.values()}:
        _validate_key_words(key=key)

    composite_pk: str = _build_composite_key(
        template=facet.pk_alias,
        values=pk_values
    )
    composite_sk: str = _build_composite_key(
        template=facet.sk_alias,
        values=sk_values
    )

    return PrimaryKey(
        partition_key=composite_pk,
        sort_key=composite_sk,
    )


def _build_root(
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
        historic_prefix='STATE',
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
    branch: str,
    group_name: str,
    url: str,
) -> Optional[RootItem]:
    primary_key = _build_key(
        facet=TABLE.facets['root_metadata'],
        pk_values={'url': url, 'branch': branch},
        sk_values={'name': group_name},
    )

    index = TABLE.indexes['inverted_index']
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key) &
            Key(key_structure.sort_key).begins_with(primary_key.partition_key)
        ),
        facets=(
            TABLE.facets['root_metadata'],
            TABLE.facets['root_historic_cloning'],
            TABLE.facets['root_historic_state']
        ),
        index=index,
        table=TABLE
    )

    if results:
        return _build_root(
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            raw_items=results
        )

    return None


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    primary_key = _build_key(
        facet=TABLE.facets['root_metadata'],
        pk_values={},
        sk_values={'name': group_name},
    )

    index = TABLE.indexes['inverted_index']
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key) &
            Key(key_structure.sort_key).begins_with(primary_key.partition_key)
        ),
        facets=(
            TABLE.facets['root_metadata'],
            TABLE.facets['root_historic_cloning'],
            TABLE.facets['root_historic_state']
        ),
        index=index,
        table=TABLE
    )

    root_items = defaultdict(lambda: [])
    for item in results:
        root_id = '#'.join(item[key_structure.sort_key].split('#')[:3])
        root_items[root_id].append(item)

    return tuple(
        _build_root(
            item_id=root_id,
            key_structure=key_structure,
            raw_items=tuple(items)
        )
        for root_id, items in root_items.items()
    )


async def create_root(
    *,
    cloning: RootHistoricCloning,
    group_name: str,
    metadata: RootMetadata,
    state: RootHistoricState
) -> None:
    key_structure = TABLE.primary_key

    metadata_key = _build_key(
        facet=TABLE.facets['root_metadata'],
        pk_values={'url': metadata.url, 'branch': metadata.branch},
        sk_values={'name': group_name},
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **dict(metadata._asdict())
    }

    historic_cloning_key = _build_key(
        facet=TABLE.facets['root_historic_cloning'],
        pk_values={
            'url': metadata.url,
            'branch': metadata.branch,
            'iso8601utc': cloning.modified_date
        },
        sk_values={'name': group_name},
    )
    initial_historic_cloning = {
        key_structure.partition_key: historic_cloning_key.partition_key,
        key_structure.sort_key: historic_cloning_key.sort_key,
        **dict(cloning._asdict())
    }

    historic_state_key = _build_key(
        facet=TABLE.facets['root_historic_state'],
        pk_values={
            'url': metadata.url,
            'branch': metadata.branch,
            'iso8601utc': state.modified_date
        },
        sk_values={'name': group_name},
    )
    initial_historic_state = {
        key_structure.partition_key: historic_state_key.partition_key,
        key_structure.sort_key: historic_state_key.sort_key,
        **dict(state._asdict())
    }

    await operations.batch_write_item(
        items=(
            initial_metadata,
            initial_historic_cloning,
            initial_historic_state
        ),
        table=TABLE
    )


async def update_root_state(
    *,
    branch: str,
    group_name: str,
    state: RootHistoricState,
    url: str
) -> None:
    key_structure = TABLE.primary_key
    historic_state_key = _build_key(
        facet=TABLE.facets['root_historic_state'],
        pk_values={
            'url': url,
            'branch': branch,
            'iso8601utc': state.modified_date
        },
        sk_values={'name': group_name},
    )

    await operations.put_item(
        item={
            key_structure.partition_key: historic_state_key.partition_key,
            key_structure.sort_key: historic_state_key.sort_key,
            **dict(state._asdict())
        },
        table=TABLE
    )


async def update_root_cloning(
    *,
    branch: str,
    cloning: RootHistoricCloning,
    group_name: str,
    url: str
) -> None:
    key_structure = TABLE.primary_key
    historic_state_key = _build_key(
        facet=TABLE.facets['root_historic_cloning'],
        pk_values={
            'url': url,
            'branch': branch,
            'iso8601utc': cloning.modified_date
        },
        sk_values={'name': group_name},
    )

    await operations.put_item(
        item={
            key_structure.partition_key: historic_state_key.partition_key,
            key_structure.sort_key: historic_state_key.sort_key,
            **dict(cloning._asdict())
        },
        table=TABLE
    )
