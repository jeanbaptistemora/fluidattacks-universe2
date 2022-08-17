from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from context import (
    FI_AWS_S3_MIRRORS_BUCKET,
)
from custom_exceptions import (
    RootNotFound,
)
from datetime import (
    datetime,
)
from db_model import (
    TABLE,
)
from db_model.roots.constants import (
    ORG_INDEX_METADATA,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitEnvironmentCloud,
    GitEnvironmentUrl,
    GitEnvironmentUrlType,
    GitRootCloning,
    MachineFindingResult,
    Root,
    RootMachineExecution,
    RootState,
    Secret,
)
from db_model.roots.utils import (
    format_cloning,
    format_root,
)
from dynamodb import (
    keys,
    operations,
)
from itertools import (
    chain,
)
from s3.operations import (
    list_files,
)
from s3.resource import (
    get_s3_resource,
)
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)


async def _get_roots(*, root_ids: List[Tuple[str, str]]) -> Tuple[Root, ...]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["git_root_metadata"],
            values={"name": group_name, "uuid": root_id},
        )
        for group_name, root_id in root_ids
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    if len(items) == len(root_ids):
        return tuple(format_root(item) for item in items)

    raise RootNotFound()


class RootLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_ids: List[Tuple[str, str]]
    ) -> Tuple[Root, ...]:
        roots = {root.id: root for root in await _get_roots(root_ids=root_ids)}

        return tuple(roots[root_id] for _, root_id in root_ids)


async def _get_group_roots(*, group_name: str) -> Tuple[Root, ...]:
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

    return tuple(format_root(item) for item in response.items)


class GroupRootsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[Root, ...], ...]:
        return await collect(
            _get_group_roots(group_name=group_name)
            for group_name in group_names
        )


async def _get_organization_roots(
    *, organization_name: str
) -> Tuple[Root, ...]:
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
        index=index,
        table=TABLE,
    )

    return tuple(format_root(item) for item in response.items)


class OrganizationRootsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_names: List[str]
    ) -> Tuple[Tuple[Root, ...], ...]:
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
            nickname=state.get("nickname"),
            other=state.get("other"),
            reason=state.get("reason"),
            status=RootStatus[state["status"]],
        )
        for state in response.items
    )


async def _get_historic_cloning(*, root_id: str) -> Tuple[GitRootCloning, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_historic_cloning"],
        values={"uuid": root_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["git_root_historic_cloning"],),
        table=TABLE,
    )

    return tuple(format_cloning(state) for state in response.items)


class RootHistoricStatesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_ids: List[str]
    ) -> Tuple[Tuple[RootState, ...], ...]:
        return await collect(
            _get_historic_state(root_id=root_id) for root_id in root_ids
        )


class RootHistoricCloningLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_ids: List[str]
    ) -> Tuple[Tuple[GitRootCloning, ...], ...]:
        return await collect(
            _get_historic_cloning(root_id=root_id) for root_id in root_ids
        )


async def get_machine_executions(
    *, root_id: str, job_id: Optional[str] = None
) -> Tuple[RootMachineExecution, ...]:
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
        RootMachineExecution(
            job_id=item["sk"].split("#")[-1],
            created_at=item["created_at"],
            started_at=item.get("started_at"),
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
            status=item.get("status"),
        )
        for item in response.items
    )


async def get_machine_executions_by_job_id(
    *, job_id: str, root_id: Optional[str] = None
) -> Tuple[RootMachineExecution, ...]:
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
        RootMachineExecution(
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
            status=item.get("status"),
        )
        for item in response.items
    )


class RootMachineExecutionsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_ids: List[str]
    ) -> Tuple[Tuple[RootMachineExecution, ...], ...]:
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
    client = await get_s3_resource()
    file_exits = bool(
        await list_files(
            bucket=FI_AWS_S3_MIRRORS_BUCKET,
            name=f"{group_name}/{root_nickname}.tar.gz",
        )
    )
    if not file_exits:
        return None

    return await client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": FI_AWS_S3_MIRRORS_BUCKET, "Key": object_name},
        ExpiresIn=1800,
    )


async def get_upload_url(group_name: str, root_nickname: str) -> Optional[str]:
    object_name = f"{group_name}/{root_nickname}.tar.gz"
    client = await get_s3_resource()

    return await client.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": FI_AWS_S3_MIRRORS_BUCKET, "Key": object_name},
        ExpiresIn=1800,
    )


async def get_upload_url_post(
    group_name: str, root_nickname: str
) -> Dict[str, Dict[str, str]]:
    object_name = f"{group_name}/{root_nickname}.tar.gz"
    client = await get_s3_resource()

    return await client.generate_presigned_post(
        FI_AWS_S3_MIRRORS_BUCKET,
        object_name,
        ExpiresIn=1800,
    )


async def get_secrets(
    *, root_id: str, secret_key: Optional[str] = None
) -> Tuple[Secret, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_secret"],
        values={
            "uuid": root_id,
            **({"key": secret_key} if secret_key else {}),
        },
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
        facets=(TABLE.facets["root_secret"],),
        table=TABLE,
    )
    return tuple(
        Secret(
            key=item["key"],
            value=item["value"],
            description=item.get("description"),
        )
        for item in response.items
    )


async def get_environment_secrets(
    *, url_id: str, secret_key: Optional[str] = None
) -> Tuple[Secret, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_environment_secret"],
        values={
            "hash": url_id,
            **({"key": secret_key} if secret_key else {}),
        },
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
        facets=(TABLE.facets["git_environment_secret"],),
        table=TABLE,
    )
    return tuple(
        Secret(
            key=item["key"],
            value=item["value"],
            description=item.get("description"),
            created_at=datetime.fromisoformat(item["created_at"])
            if "created_at" in item
            else None,
        )
        for item in response.items
    )


async def get_git_environment_urls(
    *, root_id: str, url_id: Optional[str] = None
) -> Tuple[GitEnvironmentUrl, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_environment_url"],
        values={
            "uuid": root_id,
            **({"hash": url_id} if url_id else {}),
        },
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & (
                Key(key_structure.sort_key).eq(primary_key.sort_key)
                if url_id
                else Key(key_structure.sort_key).begins_with(
                    primary_key.sort_key
                )
            )
        ),
        facets=(TABLE.facets["git_root_environment_url"],),
        table=TABLE,
    )
    return tuple(
        GitEnvironmentUrl(
            url=item["url"],
            id=item["sk"].split("URL#")[-1],
            created_at=datetime.fromisoformat(item["created_at"])
            if "created_at" in item
            else None,
            url_type=GitEnvironmentUrlType[item["type"]],
            cloud_name=GitEnvironmentCloud[item["cloud_name"]]
            if "cloud_name" in item
            else None,
        )
        for item in response.items
    )


async def get_git_environment_url_by_id(
    *, url_id: str, root_id: Optional[str] = None
) -> Optional[GitEnvironmentUrl]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_environment_url"],
        values={
            "hash": url_id,
            **({"uuid": root_id} if root_id else {}),
        },
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.sort_key).eq(primary_key.sort_key)
            & (
                Key(key_structure.partition_key).eq(primary_key.partition_key)
                if root_id
                else Key(key_structure.partition_key).begins_with(
                    primary_key.partition_key
                )
            )
        ),
        facets=(TABLE.facets["git_root_environment_url"],),
        table=TABLE,
        index=index,
    )
    if not response.items:
        return None
    item = response.items[0]
    return GitEnvironmentUrl(
        url=item["url"],
        id=item["sk"].split("URL#")[-1],
        created_at=datetime.fromisoformat(item["created_at"])
        if "created_at" in item
        else None,
        url_type=GitEnvironmentUrlType[item["type"]],
        cloud_name=GitEnvironmentCloud[item["cloud_name"]]
        if "cloud_name" in item
        else None,
    )


class RootSecretsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_ids: List[str]
    ) -> Tuple[Tuple[Secret, ...], ...]:
        return await collect(
            get_secrets(root_id=root_id) for root_id in root_ids
        )


class GitEnvironmentSecretsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, urls_ids: List[str]
    ) -> Tuple[Tuple[Secret, ...], ...]:
        return await collect(
            get_environment_secrets(url_id=url_id) for url_id in urls_ids
        )


class GitEnvironmentUrlsLoader(DataLoader):
    async def load_many_chained(
        self, root_ids: List[str]
    ) -> Tuple[GitEnvironmentUrl, ...]:
        unchained_data = await self.load_many(root_ids)
        return tuple(chain.from_iterable(unchained_data))

    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, root_ids: List[str]
    ) -> Tuple[Tuple[GitEnvironmentUrl, ...], ...]:
        return await collect(
            get_git_environment_urls(root_id=root_id) for root_id in root_ids
        )
