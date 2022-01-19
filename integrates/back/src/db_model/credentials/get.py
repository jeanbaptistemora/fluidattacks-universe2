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
    CredentialNotFound,
)
from db_model import (
    TABLE,
)
from db_model.credentials.types import (
    CredentialItem,
    CredentialMetadata,
    CredentialState,
)
from db_model.enums import (
    CredentialType,
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


def _build_credential(
    *,
    group_name: str,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> CredentialItem:
    metadata = historics.get_metadata(
        item_id=item_id, key_structure=key_structure, raw_items=raw_items
    )
    state = historics.get_latest(
        item_id=item_id,
        key_structure=key_structure,
        historic_suffix="STATE",
        raw_items=raw_items,
    )

    return CredentialItem(
        group_name=group_name,
        id=item_id,
        metadata=CredentialMetadata(
            type=CredentialType(metadata["type"]),
        ),
        state=CredentialState(
            key=state["key"],
            modified_by=state["modified_by"],
            modified_date=state["modified_date"],
            name=state["name"],
            roots=state["roots"],
        ),
    )


async def _get_credential(
    *,
    group_name: str,
    credential_id: str,
) -> CredentialItem:
    primary_key = keys.build_key(
        facet=TABLE.facets["credentials_metadata"],
        values={"name": group_name, "uuid": credential_id},
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
            TABLE.facets["credentials_historic_state"],
            TABLE.facets["credentials_metadata"],
            TABLE.facets["credentials_state"],
        ),
        index=index,
        table=TABLE,
    )

    if response.items:
        return _build_credential(
            group_name=group_name,
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            raw_items=response.items,
        )

    raise CredentialNotFound()


class CredentialLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, credential_ids: List[Tuple[str, str]]
    ) -> Tuple[CredentialItem, ...]:
        return await collect(
            _get_credential(group_name=group_name, credential_id=credential_id)
            for group_name, credential_id in credential_ids
        )


async def _get_credentials(*, group_name: str) -> Tuple[CredentialItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["credentials_metadata"],
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
            TABLE.facets["credentials_historic_state"],
            TABLE.facets["credentials_metadata"],
            TABLE.facets["credentials_state"],
        ),
        index=index,
        table=TABLE,
    )

    credential_items = defaultdict(list)
    for item in response.items:
        credential_id = "#".join(item[key_structure.sort_key].split("#")[:2])
        credential_items[credential_id].append(item)

    return tuple(
        _build_credential(
            group_name=group_name,
            item_id=credential_id,
            key_structure=key_structure,
            raw_items=tuple(items),
        )
        for credential_id, items in credential_items.items()
    )


class GroupCredentialsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[CredentialItem, ...], ...]:
        return await collect(
            _get_credentials(group_name=group_name)
            for group_name in group_names
        )


async def _get_historic_state(
    *, credential_id: str
) -> Tuple[CredentialState, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["credentials_historic_state"],
        values={"uuid": credential_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["credentials_historic_state"],),
        table=TABLE,
    )

    return tuple(
        CredentialState(
            key=state["key"],
            modified_by=state["modified_by"],
            modified_date=state["modified_date"],
            name=state["name"],
            roots=state["roots"],
        )
        for state in response.items
    )


class CredentialStatesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, credential_ids: List[str]
    ) -> Tuple[Tuple[CredentialState, ...], ...]:
        return await collect(
            _get_historic_state(credential_id=credential_id)
            for credential_id in credential_ids
        )
