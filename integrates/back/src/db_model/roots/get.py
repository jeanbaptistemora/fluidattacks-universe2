from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from collections import (
    defaultdict,
)
from custom_exceptions import (
    RootNotFound,
)
from db_model import (
    TABLE,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
    IPRootItem,
    IPRootMetadata,
    IPRootState,
    RootItem,
    RootState,
    URLRootItem,
    URLRootMetadata,
    URLRootState,
)
from dynamodb import (
    historics,
    keys,
    operations,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
)
from typing import (
    List,
    Tuple,
)


def _build_root(
    *,
    group_name: str,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> RootItem:
    metadata = historics.get_metadata(
        item_id=item_id, key_structure=key_structure, raw_items=raw_items
    )
    state = historics.get_latest(
        item_id=item_id,
        key_structure=key_structure,
        historic_suffix="STATE",
        raw_items=raw_items,
    )

    if metadata["type"] == "Git":
        cloning = historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="CLON",
            raw_items=raw_items,
        )

        return GitRootItem(
            cloning=GitRootCloning(
                modified_date=cloning["modified_date"],
                reason=cloning["reason"],
                status=cloning["status"],
            ),
            group_name=group_name,
            id=metadata[key_structure.sort_key].split("#")[1],
            metadata=GitRootMetadata(
                branch=metadata["branch"],
                type=metadata["type"],
                url=metadata["url"],
            ),
            state=GitRootState(
                environment=state["environment"],
                environment_urls=state["environment_urls"],
                git_environment_urls=[
                    GitEnvironmentUrl(url=item)
                    for item in state["environment_urls"]
                ],
                gitignore=state["gitignore"],
                includes_health_check=state["includes_health_check"],
                modified_by=state["modified_by"],
                modified_date=state["modified_date"],
                nickname=state["nickname"],
                other=state.get("other"),
                reason=state.get("reason"),
                status=state["status"],
            ),
        )

    if metadata["type"] == "IP":
        return IPRootItem(
            group_name=group_name,
            id=metadata[key_structure.sort_key].split("#")[1],
            metadata=IPRootMetadata(
                address=metadata["address"],
                port=metadata["port"],
                type=metadata["type"],
            ),
            state=IPRootState(
                modified_by=state["modified_by"],
                modified_date=state["modified_date"],
                nickname=state["nickname"],
                other=state.get("other"),
                reason=state.get("reason"),
                status=state["status"],
            ),
        )

    return URLRootItem(
        group_name=group_name,
        id=metadata[key_structure.sort_key].split("#")[1],
        metadata=URLRootMetadata(
            host=metadata["host"],
            path=metadata["path"],
            port=metadata["port"],
            protocol=metadata["protocol"],
            type=metadata["type"],
        ),
        state=URLRootState(
            modified_by=state["modified_by"],
            modified_date=state["modified_date"],
            nickname=state["nickname"],
            other=state.get("other"),
            reason=state.get("reason"),
            status=state["status"],
        ),
    )


async def _get_root(
    *,
    group_name: str,
    root_id: str,
) -> RootItem:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name, "uuid": root_id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["git_root_cloning"],
            TABLE.facets["git_root_metadata"],
            TABLE.facets["git_root_state"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["ip_root_state"],
            TABLE.facets["url_root_metadata"],
            TABLE.facets["url_root_state"],
        ),
        index=index,
        table=TABLE,
    )

    if results:
        return _build_root(
            group_name=group_name,
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            raw_items=results,
        )

    raise RootNotFound()


class RootLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, root_ids: List[Tuple[str, str]]
    ) -> Tuple[RootItem, ...]:
        return await collect(
            _get_root(group_name=group_name, root_id=root_id)
            for group_name, root_id in root_ids
        )


async def _get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["git_root_cloning"],
            TABLE.facets["git_root_metadata"],
            TABLE.facets["git_root_state"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["ip_root_state"],
            TABLE.facets["url_root_metadata"],
            TABLE.facets["url_root_state"],
        ),
        index=index,
        table=TABLE,
    )

    root_items = defaultdict(list)
    for item in results:
        root_id = "#".join(item[key_structure.sort_key].split("#")[:2])
        root_items[root_id].append(item)

    return tuple(
        _build_root(
            group_name=group_name,
            item_id=root_id,
            key_structure=key_structure,
            raw_items=tuple(items),
        )
        for root_id, items in root_items.items()
    )


class GroupRootsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[RootItem, ...], ...]:
        return await collect(
            _get_roots(group_name=group_name) for group_name in group_names
        )


async def _get_historic_state(*, root_id: str) -> Tuple[RootState, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_historic_state"],
        values={"uuid": root_id},
    )

    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(
            TABLE.facets["git_root_historic_state"],
            TABLE.facets["ip_root_historic_state"],
            TABLE.facets["url_root_historic_state"],
        ),
        table=TABLE,
    )

    return tuple(
        RootState(
            modified_by=state["modified_by"],
            modified_date=state["modified_date"],
            other=state.get("other"),
            reason=state.get("reason"),
            status=state["status"],
        )
        for state in results
    )


class RootStatesLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, root_ids: List[str]
    ) -> Tuple[Tuple[RootState, ...], ...]:
        return await collect(
            _get_historic_state(root_id=root_id) for root_id in root_ids
        )
