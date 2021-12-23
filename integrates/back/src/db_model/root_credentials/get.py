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
    RootCredentialNotFound,
)
from db_model import (
    TABLE,
)
from db_model.root_credentials.types import (
    RootCredentialItem,
    RootCredentialState,
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


def _build_root_credential(
    *,
    group_name: str,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> RootCredentialItem:
    metadata = historics.get_metadata(
        item_id=item_id, key_structure=key_structure, raw_items=raw_items
    )
    state = historics.get_latest(
        item_id=item_id,
        key_structure=key_structure,
        historic_suffix="STATE",
        raw_items=raw_items,
    )

    return RootCredentialItem(
        group_name=group_name,
        id=item_id,
        metadata=metadata,
        state=state,
    )


async def _get_root_credential(
    *,
    group_name: str,
    root_credential_id: str,
) -> RootCredentialItem:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_credentials_metadata"],
        values={"name": group_name, "uuid": root_credential_id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["root_credentials_historic_state"],
            TABLE.facets["root_credentials_metadata"],
            TABLE.facets["root_credentials_state"],
        ),
        index=index,
        table=TABLE,
    )

    if response.items:
        return _build_root_credential(
            group_name=group_name,
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            raw_items=response.items,
        )

    raise RootCredentialNotFound()


class RootCredentialLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_credential_ids: List[Tuple[str, str]]
    ) -> Tuple[RootCredentialItem, ...]:
        return await collect(
            _get_root_credential(
                group_name=group_name, root_credential_id=root_credential_id
            )
            for group_name, root_credential_id in root_credential_ids
        )


async def _get_roots_credentials(
    *, group_name: str
) -> Tuple[RootCredentialItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_credential_metadata"],
        values={"name": group_name},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["root_credentials_historic_state"],
            TABLE.facets["root_credentials_metadata"],
            TABLE.facets["root_credentials_state"],
        ),
        index=index,
        table=TABLE,
    )

    root_credential_items = defaultdict(list)
    for item in response.items:
        root_credential_id = "#".join(
            item[key_structure.sort_key].split("#")[:2]
        )
        root_credential_items[root_credential_id].append(item)

    return tuple(
        _build_root_credential(
            group_name=group_name,
            item_id=root_credential_id,
            key_structure=key_structure,
            raw_items=tuple(items),
        )
        for root_credential_id, items in root_credential_items.items()
    )


class GroupRootCredentialsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[RootCredentialItem, ...], ...]:
        return await collect(
            _get_roots_credentials(group_name=group_name)
            for group_name in group_names
        )


async def _get_historic_state(
    *, root_credential_id: str
) -> Tuple[RootCredentialState, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_credential_historic_state"],
        values={"uuid": root_credential_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["root_credential_historic_state"],),
        table=TABLE,
    )

    return tuple(
        RootCredentialState(
            key=state.get("key"),
            key_username=state.get("key_username"),
            modified_by=state["modified_by"],
            modified_date=state["modified_date"],
            name=state["name"],
            roots=state["roots"],
            status=state["status"],
        )
        for state in response.items
    )


class RootCredentialStatesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_credential_ids: List[str]
    ) -> Tuple[Tuple[RootCredentialState, ...], ...]:
        return await collect(
            _get_historic_state(root_credential_id=root_credential_id)
            for root_credential_id in root_credential_ids
        )
