from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from context import (
    FI_AWS_S3_MIRRORS_BUCKET,
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
from db_model.roots.constants import (
    ORG_INDEX_METADATA,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRootCloning,
    GitRootItem,
    GitRootState,
    IPRootItem,
    IPRootState,
    MachineFindingResult,
    RootItem,
    RootMachineExecutionItem,
    RootState,
    RootUnreliableIndicators,
    Secret,
    URLRootItem,
    URLRootState,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    Item,
)
from s3.operations import (
    aio_client,
    list_files,
)
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


def format_unreliable_indicators(
    item: Item,
) -> RootUnreliableIndicators:
    return RootUnreliableIndicators(
        unreliable_last_status_update=item["unreliable_last_status_update"]
    )


def _format_root(*, item: Item) -> RootItem:
    root_id = item["pk"].split("#")[1]
    group_name = item["sk"].split("#")[1]
    organization_name = item["pk_2"].split("#")[1]
    state = item["state"]
    unreliable_indicators = (
        format_unreliable_indicators(item["unreliable_indicators"])
        if "unreliable_indicators" in item
        else RootUnreliableIndicators()
    )

    if item["type"] == "Git":
        cloning = item["cloning"]

        return GitRootItem(
            cloning=GitRootCloning(
                modified_date=cloning["modified_date"],
                reason=cloning["reason"],
                status=GitCloningStatus(cloning["status"]),
                commit=cloning.get("commit"),
                commit_date=cloning.get("commit_date"),
            ),
            group_name=group_name,
            id=root_id,
            organization_name=organization_name,
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
                download_url=None,
                secrets=[],
                upload_url=None,
            ),
            type=item["type"],
            unreliable_indicators=unreliable_indicators,
        )

    if item["type"] == "IP":
        return IPRootItem(
            group_name=group_name,
            id=root_id,
            organization_name=organization_name,
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
            type=item["type"],
            unreliable_indicators=unreliable_indicators,
        )

    return URLRootItem(
        group_name=group_name,
        id=root_id,
        organization_name=organization_name,
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
        type=item["type"],
        unreliable_indicators=unreliable_indicators,
    )


async def _get_roots(
    *, root_ids: List[Tuple[str, str]]
) -> Tuple[RootItem, ...]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["git_root_metadata"],
            values={"name": group_name, "uuid": root_id},
        )
        for group_name, root_id in root_ids
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    if len(items) == len(root_ids):
        return tuple(_format_root(item=item) for item in items)

    raise RootNotFound()


class RootLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_ids: List[Tuple[str, str]]
    ) -> Tuple[RootItem, ...]:
        roots = {root.id: root for root in await _get_roots(root_ids=root_ids)}

        return tuple(roots[root_id] for _, root_id in root_ids)


async def _get_group_roots(*, group_name: str) -> Tuple[RootItem, ...]:
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
        filter_expression=Attr("type").exists(),
        index=index,
        table=TABLE,
    )

    return tuple(_format_root(item=item) for item in response.items)


class GroupRootsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[RootItem, ...], ...]:
        return await collect(
            _get_group_roots(group_name=group_name)
            for group_name in group_names
        )


async def _get_organization_roots(
    *, organization_name: str
) -> Tuple[RootItem, ...]:
    primary_key = keys.build_key(
        facet=ORG_INDEX_METADATA,
        values={"name": organization_name},
    )

    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(
            TABLE.facets["git_root_metadata"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["url_root_metadata"],
        ),
        filter_expression=Attr("type").exists(),
        index=index,
        table=TABLE,
    )

    return tuple(_format_root(item=item) for item in response.items)


class OrganizationRootsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_names: List[str]
    ) -> Tuple[Tuple[RootItem, ...], ...]:
        return await collect(
            _get_organization_roots(organization_name=organization_name)
            for organization_name in organization_names
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
        facet=TABLE.facets["machine_git_root_execution"],
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
        facets=(TABLE.facets["machine_git_root_execution"],),
        table=TABLE,
    )
    return tuple(
        RootMachineExecutionItem(
            job_id=item["sk"].split("#")[-1],
            created_at=item["created_at"],
            started_at=item["started_at"],
            stopped_at=item.get("stopped_at"),
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
        facet=TABLE.facets["machine_git_root_execution"],
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
        facets=(TABLE.facets["machine_git_root_execution"],),
        table=TABLE,
        index=index,
    )
    return tuple(
        RootMachineExecutionItem(
            job_id=item["sk"].split("#")[-1],
            created_at=item["created_at"],
            started_at=item["started_at"],
            stopped_at=item.get("stopped_at"),
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


async def get_download_url(
    group_name: str, root_nickname: str
) -> Optional[str]:
    object_name = f"{group_name}/{root_nickname}.tar.gz"
    file_exits = bool(
        await list_files(
            bucket=FI_AWS_S3_MIRRORS_BUCKET,
            name=f"{group_name}/{root_nickname}.tar.gz",
        )
    )
    if not file_exits:
        return None
    async with aio_client() as client:
        return await client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": FI_AWS_S3_MIRRORS_BUCKET, "Key": object_name},
            ExpiresIn=1800,
        )


async def get_upload_url(group_name: str, root_nickname: str) -> Optional[str]:
    object_name = f"{group_name}/{root_nickname}.tar.gz"
    async with aio_client() as client:
        return await client.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": FI_AWS_S3_MIRRORS_BUCKET, "Key": object_name},
            ExpiresIn=1800,
        )


async def get_upload_url_post(
    group_name: str, root_nickname: str
) -> Dict[str, Union[str, Dict[str, str]]]:
    object_name = f"{group_name}/{root_nickname}.tar.gz"
    async with aio_client() as client:
        return await client.generate_presigned_post(
            FI_AWS_S3_MIRRORS_BUCKET,
            object_name,
            ExpiresIn=1800,
        )


async def get_secrets(
    *, root_id: str, secret_key: Optional[str] = None
) -> Tuple[Secret, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_secret"],
        values={"uuid": root_id, "key": secret_key},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & (
                Key(key_structure.sort_key).eq(primary_key.sort_key)
                if secret_key
                else Key(key_structure.sort_key).begins_with(
                    primary_key.sort_key
                )
            )
        ),
        facets=(TABLE.facets["git_root_secret"],),
        table=TABLE,
    )
    return tuple(
        Secret(key=item["key"], value=item["value"]) for item in response.items
    )


class RootSecretsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_ids: List[str]
    ) -> Tuple[Tuple[Secret, ...], ...]:
        return await collect(
            get_secrets(root_id=root_id) for root_id in root_ids
        )
