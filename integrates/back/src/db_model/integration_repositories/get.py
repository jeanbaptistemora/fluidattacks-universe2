from .types import (
    OrganizationIntegrationRepository,
    OrganizationIntegrationRepositoryConnection,
    OrganizationIntegrationRepositoryEdge,
    OrganizationIntegrationRepositoryRequest,
)
from .utils import (
    format_organization_integration_repository,
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
    Optional,
)


async def _get_unreliable_integration_repositories(
    organization_id: str,
    url_id: Optional[str] = None,
    branch: Optional[str] = None,
) -> list[OrganizationIntegrationRepository]:
    organization_id = remove_org_id_prefix(organization_id)
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_integration_repository"],
        values={
            "id": organization_id,
            **(
                {"hash": url_id, "branch": branch} if url_id and branch else {}
            ),
        },
    )

    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & (
                Key(key_structure.sort_key).eq(primary_key.sort_key)
                if url_id and branch
                else Key(key_structure.sort_key).begins_with("URL#")
            )
        ),
        facets=(
            TABLE.facets["organization_unreliable_integration_repository"],
        ),
        table=TABLE,
    )

    if not response.items:
        return []

    return [
        format_organization_integration_repository(item)
        for item in response.items
    ]


async def _get_organization_unreliable_integration_repositories(
    request: OrganizationIntegrationRepositoryRequest,
) -> OrganizationIntegrationRepositoryConnection:
    organization_id = remove_org_id_prefix(request.organization_id)
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_integration_repository"],
        values={
            "id": organization_id,
        },
    )

    response = await operations.query(
        after=request.after,
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with("URL#")
        ),
        facets=(
            TABLE.facets["organization_unreliable_integration_repository"],
        ),
        limit=request.first,
        paginate=request.paginate,
        table=TABLE,
    )

    return OrganizationIntegrationRepositoryConnection(
        edges=tuple(
            OrganizationIntegrationRepositoryEdge(
                cursor=response.page_info.end_cursor,
                node=format_organization_integration_repository(item),
            )
            for item in response.items
        ),
        page_info=response.page_info,
    )


class OrganizationUnreliableRepositoriesLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: list[tuple[str, str, str]]
    ) -> list[list[OrganizationIntegrationRepository]]:
        return list(
            await collect(
                tuple(
                    _get_unreliable_integration_repositories(
                        organization_id=organization_id,
                        url_id=url_id,
                        branch=branch,
                    )
                    for organization_id, url_id, branch in ids
                )
            )
        )


class OrganizationUnreliableRepositoriesConnectionLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: list[OrganizationIntegrationRepositoryRequest]
    ) -> list[OrganizationIntegrationRepositoryConnection]:
        return list(
            await collect(
                tuple(
                    _get_organization_unreliable_integration_repositories(
                        request
                    )
                    for request in requests
                )
            )
        )
