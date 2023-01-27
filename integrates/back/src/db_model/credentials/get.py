from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from db_model.credentials.constants import (
    OWNER_INDEX_FACET,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
)
from db_model.credentials.utils import (
    format_credential,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
    Optional,
)


async def _get_credentials(
    *, requests: list[CredentialsRequest]
) -> list[Optional[Credentials]]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["credentials_metadata"],
            values={
                "id": request.id,
                "organization_id": request.organization_id,
            },
        )
        for request in requests
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    response = {
        (credential.id, credential.organization_id): credential
        for credential in [format_credential(item) for item in items]
    }
    return list(
        response[(request.id, request.organization_id)] for request in requests
    )


class CredentialsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: list[CredentialsRequest]
    ) -> list[Optional[Credentials]]:
        return await _get_credentials(requests=requests)


async def _get_organization_credentials(
    *, organization_id: str
) -> tuple[Credentials, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["credentials_metadata"],
        values={"organization_id": organization_id},
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
        facets=(TABLE.facets["credentials_metadata"],),
        index=index,
        table=TABLE,
    )

    return tuple(format_credential(item) for item in response.items)


class OrganizationCredentialsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_ids: Iterable[str]
    ) -> tuple[tuple[Credentials, ...], ...]:
        return await collect(
            _get_organization_credentials(organization_id=organization_id)
            for organization_id in organization_ids
        )


async def _get_user_credentials(*, user_email: str) -> tuple[Credentials, ...]:
    primary_key = keys.build_key(
        facet=OWNER_INDEX_FACET,
        values={"owner": user_email},
    )
    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(OWNER_INDEX_FACET,),
        index=index,
        table=TABLE,
    )

    return tuple(format_credential(item) for item in response.items)


class UserCredentialsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, user_emails: Iterable[str]
    ) -> tuple[tuple[Credentials, ...], ...]:
        return await collect(
            _get_user_credentials(user_email=user_email)
            for user_email in user_emails
        )
