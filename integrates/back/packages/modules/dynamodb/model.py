# Standard library
from collections import defaultdict
from typing import Optional, Tuple

# Third party
from boto3.dynamodb.conditions import Key

# Local
from dynamodb import historics, keys, operations
from dynamodb.table import TABLE
from dynamodb.types import (
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
    GitRootToeLines,
    IPRootItem,
    IPRootMetadata,
    IPRootState,
    Item,
    PrimaryKey,
    RootItem,
    URLRootItem,
    URLRootMetadata,
    URLRootState,
    VulnerabilityItem,
    VulnerabilityMetadata,
    VulnerabilityState
)


def _build_root(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> RootItem:
    metadata = historics.get_metadata(
        item_id=item_id,
        key_structure=key_structure,
        raw_items=raw_items
    )
    state = historics.get_latest(
        item_id=item_id,
        key_structure=key_structure,
        historic_prefix='STATE',
        raw_items=raw_items
    )

    if metadata['type'] == 'Git':
        cloning = historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_prefix='CLON',
            raw_items=raw_items
        )

        return GitRootItem(
            cloning=GitRootCloning(
                modified_date=cloning['modified_date'],
                reason=cloning['reason'],
                status=cloning['status']
            ),
            id=metadata[key_structure.sort_key].split('#')[1],
            metadata=GitRootMetadata(
                branch=metadata['branch'],
                type=metadata['type'],
                url=metadata['url']
            ),
            state=GitRootState(
                environment_urls=state['environment_urls'],
                environment=state['environment'],
                gitignore=state['gitignore'],
                includes_health_check=state['includes_health_check'],
                modified_by=state['modified_by'],
                modified_date=state['modified_date'],
                nickname=state['nickname'],
                status=state['status']
            )
        )

    if metadata['type'] == 'IP':
        return IPRootItem(
            id=metadata[key_structure.sort_key].split('#')[1],
            metadata=IPRootMetadata(type=metadata['type']),
            state=IPRootState(
                address=state['address'],
                modified_by=state['modified_by'],
                modified_date=state['modified_date'],
                port=state['port']
            )
        )

    return URLRootItem(
        id=metadata[key_structure.sort_key].split('#')[1],
        metadata=URLRootMetadata(type=metadata['type']),
        state=URLRootState(
            host=state['host'],
            modified_by=state['modified_by'],
            modified_date=state['modified_date'],
            path=state['path'],
            port=state['port'],
            protocol=state['protocol']
        )
    )


async def get_root(
    *,
    group_name: str,
    root_id: str,
) -> Optional[RootItem]:
    primary_key = keys.build_key(
        facet=TABLE.facets['root_metadata'],
        values={'name': group_name, 'uuid': root_id},
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

    root_items = defaultdict(list)
    for item in results:
        root_id = '#'.join(item[key_structure.sort_key].split('#')[:2])
        root_items[root_id].append(item)

    return tuple(
        _build_root(
            item_id=root_id,
            key_structure=key_structure,
            raw_items=tuple(items)
        )
        for root_id, items in root_items.items()
    )


async def create_root(*, group_name: str, root: RootItem) -> None:
    key_structure = TABLE.primary_key

    metadata_key = keys.build_key(
        facet=TABLE.facets['root_metadata'],
        values={'name': group_name, 'uuid': root.id},
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **dict(root.metadata._asdict())
    }

    historic_state = historics.build_historic(
        attributes=dict(root.state._asdict()),
        historic_facet=TABLE.facets['root_historic_state'],
        key_structure=key_structure,
        key_values={
            'iso8601utc': root.state.modified_date,
            'name': group_name,
            'uuid': root.id
        },
        latest_facet=TABLE.facets['root_state'],
    )

    items = (initial_metadata, *historic_state)

    if isinstance(root, GitRootItem):
        historic_cloning = historics.build_historic(
            attributes=dict(root.cloning._asdict()),
            historic_facet=TABLE.facets['root_historic_cloning'],
            key_structure=key_structure,
            key_values={
                'iso8601utc': root.cloning.modified_date,
                'name': group_name,
                'uuid': root.id
            },
            latest_facet=TABLE.facets['root_cloning'],
        )
        await operations.batch_write_item(
            items=(*items, *historic_cloning),
            table=TABLE
        )
    else:
        await operations.batch_write_item(items=items, table=TABLE)


async def update_git_root_state(
    *,
    group_name: str,
    root_id: str,
    state: GitRootState
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=dict(state._asdict()),
        historic_facet=TABLE.facets['root_historic_state'],
        key_structure=key_structure,
        key_values={
            'iso8601utc': state.modified_date,
            'name': group_name,
            'uuid': root_id
        },
        latest_facet=TABLE.facets['root_state'],
    )

    await operations.batch_write_item(items=historic, table=TABLE)


async def update_git_root_cloning(
    *,
    cloning: GitRootCloning,
    group_name: str,
    root_id: str
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=dict(cloning._asdict()),
        historic_facet=TABLE.facets['root_historic_cloning'],
        key_structure=key_structure,
        key_values={
            'iso8601utc': cloning.modified_date,
            'name': group_name,
            'uuid': root_id
        },
        latest_facet=TABLE.facets['root_cloning'],
    )

    await operations.batch_write_item(items=historic, table=TABLE)


async def delete_git_root_toe_lines(
    *,
    filename: str,
    group_name: str,
    root_id: str
) -> None:
    facet = TABLE.facets['root_toe_lines']
    toe_lines_key = keys.build_key(
        facet=facet,
        values={
            'filename': filename,
            'group_name': group_name,
            'root_id': root_id,
        },
    )
    await operations.delete_item(
        primary_key=toe_lines_key,
        table=TABLE
    )


def _build_git_root_toe_lines(
    *,
    group_name: str,
    key_structure: PrimaryKey,
    item: Item,
) -> GitRootToeLines:
    sort_key_items = item[key_structure.sort_key].split('#')
    root_id = sort_key_items[1]
    filename = sort_key_items[3]
    return GitRootToeLines(
        comments=item['comments'],
        filename=filename,
        group_name=group_name,
        loc=item['loc'],
        modified_commit=item['modified_commit'],
        modified_date=item['modified_date'],
        root_id=root_id,
        tested_date=item['tested_date'],
        tested_lines=item['tested_lines'],
    )


async def get_toe_lines_by_root(
    *,
    group_name: str,
    root_id: str
) -> Tuple[GitRootToeLines, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets['root_toe_lines'],
        values={'group_name': group_name, 'root_id': root_id},
    )
    key_structure = TABLE.primary_key
    root_key = '#'.join(primary_key.sort_key.split('#')[:2])
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key) &
            Key(key_structure.sort_key).begins_with(root_key)
        ),
        facets=(
            TABLE.facets['root_toe_lines'],
        ),
        index=None,
        table=TABLE
    )
    return tuple(
        _build_git_root_toe_lines(
            group_name=group_name,
            key_structure=key_structure,
            item=item
        )
        for item in results
    )


async def update_git_root_toe_lines(
    *,
    root_toe_lines: GitRootToeLines
) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets['root_toe_lines']
    toe_lines_key = keys.build_key(
        facet=facet,
        values={
            'filename': root_toe_lines.filename,
            'group_name': root_toe_lines.group_name,
            'root_id': root_toe_lines.root_id,
        },
    )
    toe_lines = {
        key_structure.partition_key: toe_lines_key.partition_key,
        key_structure.sort_key: toe_lines_key.sort_key,
        **dict(root_toe_lines._asdict())
    }
    await operations.put_item(
        facet=facet,
        item=toe_lines,
        table=TABLE
    )


def _build_vuln(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> VulnerabilityItem:
    metadata = historics.get_metadata(
        item_id=item_id,
        key_structure=key_structure,
        raw_items=raw_items
    )
    state = historics.get_latest(
        item_id=item_id,
        key_structure=key_structure,
        historic_prefix='STATE',
        raw_items=raw_items
    )

    return VulnerabilityItem(
        id=metadata[key_structure.sort_key].split('#')[1],
        metadata=VulnerabilityMetadata(
            affected_components=metadata['affected_components'],
            attack_vector=metadata['attack_vector'],
            cvss=metadata['cvss'],
            cwe=metadata['cwe'],
            description=metadata['description'],
            evidences=metadata['evidences'],
            name=metadata['name'],
            recommendation=metadata['recommendation'],
            requirements=metadata['requirements'],
            source=metadata['source'],
            specific=metadata['specific'],
            threat=metadata['threat'],
            type=metadata['type'],
            using_sorts=metadata['using_sorts'],
            where=metadata['where']
        ),
        state=VulnerabilityState(
            modified_by=state['modified_by'],
            modified_date=state['modified_date'],
            reason=state['reason'],
            source=state['source'],
            status=state['status'],
            tags=state['tags']
        )
    )


async def get_vulnerabilities(
    *,
    root: GitRootItem
) -> Tuple[VulnerabilityItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets['vulnerability_metadata'],
        values={'root_uuid': root.id},
    )

    index = TABLE.indexes['inverted_index']
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key) &
            Key(key_structure.sort_key).begins_with(primary_key.partition_key)
        ),
        facets=(
            TABLE.facets['vulnerability_metadata'],
            TABLE.facets['vulnerability_state']
        ),
        index=index,
        table=TABLE
    )

    vuln_items = defaultdict(list)
    for item in results:
        vuln_id = '#'.join(item[key_structure.sort_key].split('#')[:2])
        vuln_items[vuln_id].append(item)

    return tuple(
        _build_vuln(
            item_id=vuln_id,
            key_structure=key_structure,
            raw_items=tuple(items)
        )
        for vuln_id, items in vuln_items.items()
    )
