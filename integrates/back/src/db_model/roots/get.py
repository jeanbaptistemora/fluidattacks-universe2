from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
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
    RootItem,
    RootMachineExecutionItem,
    RootState,
    URLRootItem,
    URLRootMetadata,
    URLRootState,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
)
from typing import (
    List,
    Optional,
    Tuple,
)


def _format_root(*, item: Item) -> RootItem:
    root_id = item["pk"].split("#")[1]
    group_name = item["sk"].split("#")[1]
    state = item["state"]

    if item["type"] == "Git":
        cloning = item["cloning"]

        return GitRootItem(
            cloning=GitRootCloning(
                modified_date=cloning["modified_date"],
                reason=cloning["reason"],
                status=GitCloningStatus(cloning["status"]),
                commit=cloning.get("commit"),
            ),
            group_name=group_name,
            id=root_id,
            metadata=GitRootMetadata(type=item["type"]),
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

    if item["type"] == "IP":
        return IPRootItem(
            group_name=group_name,
            id=root_id,
            metadata=IPRootMetadata(type=item["type"]),
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
        id=root_id,
        metadata=URLRootMetadata(type=item["type"]),
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

    item = await operations.get_item(
        facets=(
            TABLE.facets["git_root_metadata"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["url_root_metadata"],
        ),
        key=primary_key,
        table=TABLE,
    )

    if item:
        return _format_root(item=item)

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
            TABLE.facets["git_root_metadata"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["url_root_metadata"],
        ),
        index=index,
        table=TABLE,
    )

    return tuple(
        _format_root(item=item)
        for item in response.items
        # Needed while we finish the cleanup of old items
        if len(item["pk"].split("#")) == 2
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
    ) -> Tuple[Tuple[RootMachineExecutionItem, ...], ...]:
        machine_executions = await collect(
            get_machine_executions(root_id=root_id) for root_id in root_ids
        )
        return tuple(
            tuple(sorted(execution, key=lambda x: x.created_at, reverse=True))
            for execution in machine_executions
        )
