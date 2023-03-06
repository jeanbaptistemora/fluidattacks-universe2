from .types import (
    GroupAccess,
    GroupAccessRequest,
)
from .utils import (
    format_group_access,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from collections.abc import (
    Iterable,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def _get_group_access(
    *, requests: Iterable[GroupAccessRequest]
) -> list[GroupAccess | None]:
    requests_formatted = [
        request._replace(
            group_name=request.group_name.lower().strip(),
            email=request.email.lower().strip(),
        )
        for request in requests
    ]
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["group_access"],
            values={
                "email": request.email,
                "name": request.group_name,
            },
        )
        for request in requests_formatted
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    response = {
        GroupAccessRequest(
            group_name=group_access.group_name, email=group_access.email
        ): group_access
        for group_access in list(format_group_access(item) for item in items)
    }
    return [response.get(request) for request in requests_formatted]


class GroupAccessLoader(DataLoader[GroupAccessRequest, GroupAccess | None]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[GroupAccessRequest]
    ) -> list[GroupAccess | None]:
        return await _get_group_access(requests=requests)


async def _get_historic_group_access(
    *, request: GroupAccessRequest
) -> list[GroupAccess]:
    historic_key = keys.build_key(
        facet=TABLE.facets["group_historic_access"],
        values={
            "email": request.email.lower().strip(),
            "name": request.group_name.lower().strip(),
        },
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        historic_key.partition_key
    ) & Key(key_structure.sort_key).begins_with(historic_key.sort_key)
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(TABLE.facets["group_historic_access"],),
        table=TABLE,
    )

    return [format_group_access(item) for item in response.items]


class GroupHistoricAccessLoader(
    DataLoader[GroupAccessRequest, list[GroupAccess]]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: Iterable[GroupAccessRequest]
    ) -> list[list[GroupAccess]]:
        return list(
            await collect(
                tuple(
                    _get_historic_group_access(request=request)
                    for request in requests
                )
            )
        )


async def _get_group_stakeholders_access(
    *,
    access_dataloader: GroupAccessLoader,
    group_name: str,
) -> list[GroupAccess]:
    group_name = group_name.lower().strip()
    primary_key = keys.build_key(
        facet=TABLE.facets["group_access"],
        values={
            "name": group_name,
        },
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
        facets=(TABLE.facets["group_access"],),
        table=TABLE,
        index=index,
    )

    access_list: list[GroupAccess] = []
    for item in response.items:
        access = format_group_access(item)
        access_list.append(access)
        access_dataloader.prime(
            GroupAccessRequest(group_name=group_name, email=access.email),
            access,
        )

    return access_list


class GroupStakeholdersAccessLoader(DataLoader[str, list[GroupAccess]]):
    def __init__(self, dataloader: GroupAccessLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> list[list[GroupAccess]]:
        return list(
            await collect(
                tuple(
                    _get_group_stakeholders_access(
                        access_dataloader=self.dataloader,
                        group_name=group_name,
                    )
                    for group_name in group_names
                )
            )
        )


async def _get_stakeholder_groups_access(
    *,
    access_dataloader: GroupAccessLoader,
    email: str,
) -> list[GroupAccess]:
    email = email.lower().strip()
    primary_key = keys.build_key(
        facet=TABLE.facets["group_access"],
        values={
            "email": email,
        },
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["group_access"],),
        table=TABLE,
    )

    access_list: list[GroupAccess] = []
    for item in response.items:
        access = format_group_access(item)
        access_list.append(access)
        access_dataloader.prime(
            GroupAccessRequest(group_name=access.group_name, email=email),
            access,
        )

    return access_list


class StakeholderGroupsAccessLoader(DataLoader[str, list[GroupAccess]]):
    def __init__(self, dataloader: GroupAccessLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> list[list[GroupAccess]]:
        return list(
            await collect(
                tuple(
                    _get_stakeholder_groups_access(
                        access_dataloader=self.dataloader, email=email
                    )
                    for email in emails
                )
            )
        )
