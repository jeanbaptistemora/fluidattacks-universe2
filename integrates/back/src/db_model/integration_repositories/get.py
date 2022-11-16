# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from .types import (
    OrganizationIntegrationRepository,
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
    Iterable,
    Optional,
)


async def _get_unreliable_integration_repositories(
    organization_id: str,
    url_id: Optional[str] = None,
    branch: Optional[str] = None,
) -> tuple[OrganizationIntegrationRepository, ...]:
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
        return tuple()

    return tuple(
        format_organization_integration_repository(item)
        for item in response.items
    )


class OrganizationUnreliableRepositoriesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Iterable[tuple[str, str, str]]
    ) -> tuple[tuple[OrganizationIntegrationRepository, ...], ...]:
        return await collect(
            tuple(
                _get_unreliable_integration_repositories(
                    organization_id=organization_id,
                    url_id=url_id,
                    branch=branch,
                )
                for organization_id, url_id, branch in ids
            )
        )
