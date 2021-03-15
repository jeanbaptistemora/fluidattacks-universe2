# Standard library
from collections import defaultdict
from typing import Optional, Tuple

# Third party
from boto3.dynamodb.conditions import Key

# Local
from dynamodb import historics, keys, operations
from dynamodb.table import TABLE
from dynamodb.types import (
    Item,
    PrimaryKey,
    RootCloning,
    RootState,
    RootItem,
    RootMetadata
)


def _build_root(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> RootItem:
    cloning = historics.get_latest(
        item_id=item_id,
        key_structure=key_structure,
        historic_prefix='CLON',
        raw_items=raw_items
    )
    state = historics.get_latest(
        item_id=item_id,
        key_structure=key_structure,
        historic_prefix='STATE',
        raw_items=raw_items
    )
    metadata = historics.get_metadata(
        item_id=item_id,
        key_structure=key_structure,
        raw_items=raw_items
    )

    return RootItem(
        cloning=RootCloning(
            modified_date=cloning['modified_date'],
            reason=cloning['reason'],
            status=cloning['status']
        ),
        state=RootState(
            environment_urls=state['environment_urls'],
            environment=state['environment'],
            gitignore=state['gitignore'],
            includes_health_check=state['includes_health_check'],
            modified_by=state['modified_by'],
            modified_date=state['modified_date'],
            status=state['status']
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
    primary_key = keys.build_key(
        facet=TABLE.facets['root_metadata'],
        values={'branch': branch, 'name': group_name, 'url': url},
    )

    index = TABLE.indexes['inverted_index']
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key) &
            Key(key_structure.sort_key).begins_with(primary_key.partition_key)
        ),
        facets=(
            TABLE.facets['root_cloning'],
            TABLE.facets['root_metadata'],
            TABLE.facets['root_state']
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
    primary_key = keys.build_key(
        facet=TABLE.facets['root_metadata'],
        values={'name': group_name},
    )

    index = TABLE.indexes['inverted_index']
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key) &
            Key(key_structure.sort_key).begins_with(primary_key.partition_key)
        ),
        facets=(
            TABLE.facets['root_cloning'],
            TABLE.facets['root_metadata'],
            TABLE.facets['root_state']
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
    cloning: RootCloning,
    group_name: str,
    metadata: RootMetadata,
    state: RootState
) -> None:
    key_structure = TABLE.primary_key

    metadata_key = keys.build_key(
        facet=TABLE.facets['root_metadata'],
        values={
            'branch': metadata.branch,
            'name': group_name,
            'url': metadata.url
        },
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **dict(metadata._asdict())
    }

    historic_cloning = historics.build_historic(
        attributes=dict(cloning._asdict()),
        historic_facet=TABLE.facets['root_historic_cloning'],
        key_structure=key_structure,
        key_values={
            'branch': metadata.branch,
            'iso8601utc': cloning.modified_date,
            'name': group_name,
            'url': metadata.url
        },
        latest_facet=TABLE.facets['root_cloning'],
    )

    historic_state = historics.build_historic(
        attributes=dict(state._asdict()),
        historic_facet=TABLE.facets['root_historic_state'],
        key_structure=key_structure,
        key_values={
            'branch': metadata.branch,
            'iso8601utc': state.modified_date,
            'name': group_name,
            'url': metadata.url
        },
        latest_facet=TABLE.facets['root_state'],
    )

    await operations.batch_write_item(
        items=(
            initial_metadata,
            *historic_cloning,
            *historic_state
        ),
        table=TABLE
    )


async def update_root_state(
    *,
    branch: str,
    group_name: str,
    state: RootState,
    url: str
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=dict(state._asdict()),
        historic_facet=TABLE.facets['root_historic_state'],
        key_structure=key_structure,
        key_values={
            'branch': branch,
            'iso8601utc': state.modified_date,
            'name': group_name,
            'url': url
        },
        latest_facet=TABLE.facets['root_state'],
    )

    await operations.batch_write_item(items=historic, table=TABLE)


async def update_root_cloning(
    *,
    branch: str,
    cloning: RootCloning,
    group_name: str,
    url: str
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=dict(cloning._asdict()),
        historic_facet=TABLE.facets['root_historic_cloning'],
        key_structure=key_structure,
        key_values={
            'branch': branch,
            'iso8601utc': cloning.modified_date,
            'name': group_name,
            'url': url
        },
        latest_facet=TABLE.facets['root_cloning'],
    )

    await operations.batch_write_item(items=historic, table=TABLE)
