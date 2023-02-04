from .constants import (
    ALL_ORGANIZATIONS_INDEX_METADATA,
    ORGANIZATION_ID_PREFIX,
)
from .types import (
    Organization,
    OrganizationUnreliableIndicators,
)
from .utils import (
    format_organization,
    format_unreliable_indicators,
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
    ErrorLoadingOrganizations,
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
    AsyncIterator,
    Iterable,
    Optional,
)


async def get_all_organizations() -> list[Organization]:
    primary_key = keys.build_key(
        facet=ALL_ORGANIZATIONS_INDEX_METADATA,
        values={"all": "all"},
    )
    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(ALL_ORGANIZATIONS_INDEX_METADATA,),
        table=TABLE,
        index=index,
    )

    if not response.items:
        raise ErrorLoadingOrganizations()

    return [format_organization(item) for item in response.items]


async def iterate_organizations() -> AsyncIterator[Organization]:
    for organization in await get_all_organizations():
        yield organization


async def _get_organization_by_id(
    *, organization_id: str
) -> Optional[Organization]:
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
        return None

    return format_organization(response.items[0])


async def _get_organization_by_name(
    *, organization_name: str
) -> Optional[Organization]:
    organization_name = organization_name.lower().strip()
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
        return None

    return format_organization(response.items[0])


async def _get_organization(
    *, organization_key: str
) -> Optional[Organization]:
    if organization_key.startswith(ORGANIZATION_ID_PREFIX):
        return await _get_organization_by_id(organization_id=organization_key)
    return await _get_organization_by_name(organization_name=organization_key)


class OrganizationLoader(DataLoader[str, Optional[Organization]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_keys: Iterable[str]
    ) -> list[Optional[Organization]]:
        # Organizations can be loaded either by name or id(preceded by "ORG#")
        organizations = await collect(
            tuple(
                _get_organization(organization_key=key)
                for key in organization_keys
            )
        )
        for organization in organizations:
            if organization:
                self.prime(organization.id, organization)
                self.prime(organization.name, organization)

        return list(organizations)


async def _get_organization_unreliable_indicators(
    *, organization_id: str
) -> OrganizationUnreliableIndicators:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_indicators"],
        values={"id": organization_id},
    )
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with("ORG#")
        ),
        facets=(TABLE.facets["organization_unreliable_indicators"],),
        limit=1,
        table=TABLE,
    )
    if not response.items:
        return OrganizationUnreliableIndicators()

    return format_unreliable_indicators(response.items[0])


class OrganizationUnreliableIndicatorsLoader(
    DataLoader[str, OrganizationUnreliableIndicators]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, organization_ids: Iterable[str]
    ) -> list[OrganizationUnreliableIndicators]:
        return list(
            await collect(
                _get_organization_unreliable_indicators(
                    organization_id=organization_id
                )
                for organization_id in organization_ids
            )
        )
