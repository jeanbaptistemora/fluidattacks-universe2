from .constants import (
    ORGANIZATION_ID_PREFIX,
)
from .types import (
    Organization,
)
from .utils import (
    format_organization,
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
from custom_exceptions import (
    OrganizationNotFound,
)
from db_model import (
    TABLE,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def _get_organization_by_id(*, organization_id: str) -> Organization:
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_metadata"],
        values={"id": remove_org_id_prefix(organization_id)},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["organization_metadata"],),
        limit=1,
        table=TABLE,
    )

    if not response.items:
        raise OrganizationNotFound()

    return format_organization(response.items[0])


async def _get_organization_by_name(*, organization_name: str) -> Organization:
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_metadata"],
        values={"name": organization_name},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.sort_key).eq(primary_key.sort_key)
            & Key(key_structure.partition_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["organization_metadata"],),
        index=TABLE.indexes["inverted_index"],
        limit=1,
        table=TABLE,
    )

    if not response.items:
        raise OrganizationNotFound()

    return format_organization(response.items[0])


async def _get_organization(*, organization_key: str) -> Organization:
    if organization_key.startswith(ORGANIZATION_ID_PREFIX):
        return await _get_organization_by_id(organization_id=organization_key)
    return await _get_organization_by_name(organization_name=organization_key)


class OrganizationLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_keys: Iterable[str]
    ) -> tuple[Organization, ...]:
        # Organizations can be loaded either by name or id(preceded by "ORG#")
        return await collect(
            tuple(
                _get_organization(organization_key=key)
                for key in organization_keys
            )
        )
