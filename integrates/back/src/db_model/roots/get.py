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
from db_model.enums import (
    GitCloningStatus,
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
    MachineFindingResult,
    MachineGitRootExecution,
    RootItem,
    RootMachineExecutionItem,
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
    Optional,
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
        queue = [
            item
            for item in raw_items
            if item[key_structure.sort_key].startswith(f"{item_id}#FIN")
            and item[key_structure.sort_key].endswith("#MACHINE")
        ]
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
                status=GitCloningStatus(cloning["status"]),
            ),
            machine_execution=[
                MachineGitRootExecution(
                    queue_date=item.get("queue_date"),
                    job_id=item.get("job_id"),
                    finding_code=item.get("finding_code"),
                )
                for item in queue
            ],
            group_name=group_name,
            id=metadata[key_structure.sort_key].split("#")[1],
            metadata=GitRootMetadata(type=metadata["type"]),
            state=GitRootState(
                branch=state["branch"],
                environment_urls=state["environment_urls"],
                environment=state["environment"],
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
                url=state["url"],
            ),
        )

    if metadata["type"] == "IP":
        return IPRootItem(
            group_name=group_name,
            id=metadata[key_structure.sort_key].split("#")[1],
            metadata=IPRootMetadata(type=metadata["type"]),
            state=IPRootState(
                address=state["address"],
                modified_by=state["modified_by"],
                modified_date=state["modified_date"],
                nickname=state["nickname"],
                other=state.get("other"),
                port=state["port"],
                reason=state.get("reason"),
                status=state["status"],
            ),
        )

    return URLRootItem(
        group_name=group_name,
        id=metadata[key_structure.sort_key].split("#")[1],
        metadata=URLRootMetadata(type=metadata["type"]),
        state=URLRootState(
            host=state["host"],
            modified_by=state["modified_by"],
            modified_date=state["modified_date"],
            nickname=state["nickname"],
            other=state.get("other"),
            path=state["path"],
            port=state["port"],
            protocol=state["protocol"],
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
    response = await operations.query(
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
            TABLE.facets["machine_git_root_execution"],
            TABLE.facets["url_root_metadata"],
            TABLE.facets["url_root_state"],
        ),
        index=index,
        table=TABLE,
    )

    if response.items:
        return _build_root(
            group_name=group_name,
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            raw_items=response.items,
        )

    raise RootNotFound()


class RootLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
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
    response = await operations.query(
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
            TABLE.facets["machine_git_root_execution"],
            TABLE.facets["ip_root_state"],
            TABLE.facets["url_root_metadata"],
            TABLE.facets["url_root_state"],
        ),
        index=index,
        table=TABLE,
    )

    root_items = defaultdict(list)
    for item in response.items:
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
    # pylint: disable=no-self-use,method-hidden
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
    response = await operations.query(
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
        for state in response.items
    )


class RootStatesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_ids: List[str]
    ) -> Tuple[Tuple[RootState, ...], ...]:
        return await collect(
            _get_historic_state(root_id=root_id) for root_id in root_ids
        )


async def get_machine_executions(
    *, root_id: str, job_id: Optional[str] = None
) -> Tuple[RootMachineExecutionItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["machine_git_root_execution_new"],
        values={"uuid": root_id, **({"job_id": job_id} if job_id else {})},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & (
                Key(key_structure.sort_key).eq(primary_key.sort_key)
                if job_id
                else Key(key_structure.sort_key).begins_with(
                    primary_key.sort_key
                )
            )
        ),
        facets=(TABLE.facets["machine_git_root_execution_new"],),
        table=TABLE,
    )
    return tuple(
        RootMachineExecutionItem(
            job_id=item["sk"].split("#")[-1],
            created_at=item["created_at"],
            started_at=item["started_at"],
            stopped_at=item["stopped_at"],
            name=item["name"],
            root_id=item["pk"].split("#")[-1],
            queue=item["queue"],
            findings_executed=[
                MachineFindingResult(
                    finding=x["finding"],
                    open=x["open"],
                    modified=x.get("modified", 0),
                )
                for x in item["findings_executed"]
            ],
            commit=item.get("commit"),
        )
        for item in response.items
    )


async def get_machine_executions_by_job_id(
    *, job_id: str, root_id: Optional[str] = None
) -> Tuple[RootMachineExecutionItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["machine_git_root_execution_new"],
        values={"job_id": job_id, **({"uuid": root_id} if root_id else {})},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = TABLE.primary_key

    response = await operations.query(
        condition_expression=(
            Key(key_structure.sort_key).eq(primary_key.sort_key)
            & Key(key_structure.partition_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["machine_git_root_execution_new"],),
        table=TABLE,
        index=index,
    )
    return tuple(
        RootMachineExecutionItem(
            job_id=item["sk"].split("#")[-1],
            created_at=item["created_at"],
            started_at=item["started_at"],
            stopped_at=item["stopped_at"],
            name=item["name"],
            queue=item["queue"],
            root_id=item["pk"].split("#")[-1],
            findings_executed=[
                MachineFindingResult(
                    finding=x["finding"],
                    open=x["open"],
                    modified=x.get("modified", 0),
                )
                for x in item["findings_executed"]
            ],
            commit=item.get("commit", ""),
        )
        for item in response.items
    )


class RootMachineExecutionsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_ids: List[str]
    ) -> Tuple[Tuple[RootState, ...], ...]:
        return await collect(
            get_machine_executions(root_id=root_id) for root_id in root_ids
        )
