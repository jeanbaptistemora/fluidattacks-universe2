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
    FI_AWS_S3_MAIN_BUCKET,
    FI_AWS_S3_PATH_PREFIX,
)
from contextlib import (
    suppress,
)
from datetime import (
    datetime,
    timezone,
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
    GitRootCloning,
    MachineFindingResult,
    Root,
    RootEnvironmentCloud,
    RootEnvironmentUrl,
    RootEnvironmentUrlType,
    RootMachineExecution,
    RootRequest,
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
    Iterable,
    Optional,
)


async def _get_roots(*, requests: Iterable[RootRequest]) -> list[Root]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["git_root_metadata"],
            values={"name": request.group_name, "uuid": request.root_id},
        )
        for request in requests
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    return [format_root(item) for item in items]


class RootLoader(DataLoader[RootRequest, Optional[Root]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[RootRequest]
    ) -> list[Optional[Root]]:
        roots = {root.id: root for root in await _get_roots(requests=requests)}

        return [roots.get(request.root_id) for request in requests]


async def _get_group_roots(*, group_name: str) -> list[Root]:
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

    return [format_root(item) for item in response.items]


class GroupRootsLoader(DataLoader[str, list[Root]]):
    async def load_many_chained(
        self, group_names: Iterable[str]
    ) -> list[Root]:
        unchained_data = await self.load_many(group_names)
        return list(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[list[Root]]:
        return list(
            await collect(
                _get_group_roots(group_name=group_name)
                for group_name in group_names
            )
        )


async def _get_organization_roots(*, organization_name: str) -> list[Root]:
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

    return [format_root(item) for item in response.items]


class OrganizationRootsLoader(DataLoader[str, list[Root]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_names: Iterable[str]
    ) -> list[list[Root]]:
        return list(
            await collect(
                _get_organization_roots(organization_name=organization_name)
                for organization_name in organization_names
            )
        )


async def _get_historic_state(*, root_id: str) -> list[RootState]:
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

    return [
        RootState(
            modified_by=state["modified_by"],
            modified_date=datetime.fromisoformat(state["modified_date"]),
            nickname=state.get("nickname"),
            other=state.get("other"),
            reason=state.get("reason"),
            status=RootStatus[state["status"]],
        )
        for state in response.items
    ]


class RootHistoricStatesLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, root_ids: Iterable[str]
    ) -> list[list[RootState]]:
        return list(
            await collect(
                _get_historic_state(root_id=root_id) for root_id in root_ids
            )
        )


async def _get_historic_cloning(*, root_id: str) -> list[GitRootCloning]:
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

    return [format_cloning(state) for state in response.items]


class RootHistoricCloningLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, root_ids: Iterable[str]
    ) -> list[list[GitRootCloning]]:
        return list(
            await collect(
                _get_historic_cloning(root_id=root_id) for root_id in root_ids
            )
        )


async def get_machine_executions(
    *, root_id: str, job_id: Optional[str] = None
) -> list[RootMachineExecution]:
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
    result: list[RootMachineExecution] = []
    for item in response.items:
        findings = []
        with suppress(TypeError):
            findings = [
                MachineFindingResult(
                    finding=x["finding"],
                    open=x["open"],
                    modified=x.get("modified", 0),
                )
                for x in item["findings_executed"]
            ]
            result.append(
                RootMachineExecution(
                    job_id=item["sk"].split("#")[-1],
                    created_at=datetime.fromisoformat(
                        item["created_at"]
                    ).astimezone(tz=timezone.utc),
                    started_at=datetime.fromisoformat(
                        item["started_at"]
                    ).astimezone(tz=timezone.utc)
                    if item.get("started_at")
                    else None,
                    stopped_at=datetime.fromisoformat(
                        item["stopped_at"]
                    ).astimezone(tz=timezone.utc)
                    if item.get("stopped_at")
                    else None,
                    name=item["name"],
                    root_id=item["pk"].split("#")[-1],
                    queue=item["queue"],
                    findings_executed=findings,
                    commit=item.get("commit"),
                    status=item.get("status"),
                ),
            )

    return result


class RootMachineExecutionsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, root_ids: Iterable[str]
    ) -> list[list[RootMachineExecution]]:
        machine_executions = await collect(
            get_machine_executions(root_id=root_id) for root_id in root_ids
        )
        return list(
            list(sorted(execution, key=lambda x: x.created_at, reverse=True))
            for execution in machine_executions
        )


async def get_machine_executions_by_job_id(
    *, job_id: str, root_id: Optional[str] = None
) -> list[RootMachineExecution]:
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

    return [
        RootMachineExecution(
            job_id=item["sk"].split("#")[-1],
            created_at=datetime.fromisoformat(item["created_at"]).astimezone(
                tz=timezone.utc
            ),
            started_at=datetime.fromisoformat(item["started_at"]).astimezone(
                tz=timezone.utc
            )
            if item.get("started_at")
            else None,
            stopped_at=datetime.fromisoformat(item["stopped_at"]).astimezone(
                tz=timezone.utc
            )
            if item.get("stopped_at")
            else None,
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
    ]


async def get_download_url(
    group_name: str, root_nickname: str
) -> Optional[str]:
    bucket_path: str = "continuous-repositories"
    object_name = f"{group_name}/{root_nickname}.tar.gz"
    client = await get_s3_resource()
    file_exits = bool(
        await list_files(
            f"{bucket_path}/{group_name}/{root_nickname}.tar.gz",
        )
    )
    if not file_exits:
        return None

    return await client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": FI_AWS_S3_MAIN_BUCKET,
            "Key": f"{FI_AWS_S3_PATH_PREFIX}{bucket_path}/{object_name}",
        },
        ExpiresIn=1800,
    )


async def get_upload_url(group_name: str, root_nickname: str) -> Optional[str]:
    bucket_path: str = f"{FI_AWS_S3_PATH_PREFIX}continuous-repositories"
    object_name = f"{group_name}/{root_nickname}.tar.gz"
    client = await get_s3_resource()

    return await client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": FI_AWS_S3_MAIN_BUCKET,
            "Key": f"{bucket_path}/{object_name}",
        },
        ExpiresIn=1800,
    )


async def get_upload_url_post(
    group_name: str, root_nickname: str
) -> dict[str, dict[str, str]]:
    object_name = f"{group_name}/{root_nickname}.tar.gz"
    client = await get_s3_resource()

    return await client.generate_presigned_post(
        FI_AWS_S3_MAIN_BUCKET,
        f"{FI_AWS_S3_PATH_PREFIX}continuous-repositories/{object_name}",
        ExpiresIn=1800,
    )


async def _get_secrets(
    *, root_id: str, secret_key: Optional[str] = None
) -> list[Secret]:
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

    return [
        Secret(
            key=item["key"],
            value=item["value"],
            description=item.get("description"),
        )
        for item in response.items
    ]


class RootSecretsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        root_ids: Iterable[str],
    ) -> list[list[Secret]]:
        return list(
            await collect(
                _get_secrets(root_id=root_id) for root_id in root_ids
            )
        )


async def _get_environment_secrets(
    *, url_id: str, secret_key: Optional[str] = None
) -> list[Secret]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_environment_secret"],
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
        facets=(TABLE.facets["root_environment_secret"],),
        table=TABLE,
    )
    return [
        Secret(
            key=item["key"],
            value=item["value"],
            description=item.get("description"),
            created_at=datetime.fromisoformat(item["created_at"])
            if "created_at" in item
            else None,
        )
        for item in response.items
    ]


class GitEnvironmentSecretsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, urls_ids: Iterable[str]
    ) -> list[list[Secret]]:
        return list(
            await collect(
                _get_environment_secrets(url_id=url_id) for url_id in urls_ids
            )
        )


async def _get_git_environment_urls(
    *, root_id: str, url_id: Optional[str] = None
) -> list[RootEnvironmentUrl]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_environment_url"],
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
        facets=(TABLE.facets["root_environment_url"],),
        table=TABLE,
    )
    return [
        RootEnvironmentUrl(
            url=item["url"],
            id=item["sk"].split("URL#")[-1],
            created_at=datetime.fromisoformat(item["created_at"])
            if "created_at" in item
            else None,
            url_type=RootEnvironmentUrlType[item["type"]]
            if "type" in item
            else RootEnvironmentUrlType.URL,
            cloud_name=RootEnvironmentCloud[item["cloud_name"]]
            if "cloud_name" in item
            else None,
        )
        for item in response.items
    ]


class RootEnvironmentUrlsLoader(DataLoader):
    async def load_many_chained(
        self, root_ids: Iterable[str]
    ) -> list[RootEnvironmentUrl]:
        unchained_data = await self.load_many(root_ids)
        return list(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, root_ids: Iterable[str]
    ) -> list[list[RootEnvironmentUrl]]:
        return list(
            await collect(
                _get_git_environment_urls(root_id=root_id)
                for root_id in root_ids
            )
        )


async def get_git_environment_url_by_id(
    *, url_id: str, root_id: Optional[str] = None
) -> Optional[RootEnvironmentUrl]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_environment_url"],
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
        facets=(TABLE.facets["root_environment_url"],),
        table=TABLE,
        index=index,
    )
    if not response.items:
        return None
    item = response.items[0]
    return RootEnvironmentUrl(
        url=item["url"],
        id=item["sk"].split("URL#")[-1],
        created_at=datetime.fromisoformat(item["created_at"])
        if "created_at" in item
        else None,
        url_type=RootEnvironmentUrlType[item["type"]],
        cloud_name=RootEnvironmentCloud[item["cloud_name"]]
        if "cloud_name" in item
        else None,
    )
