from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from db_model.organizations.types import (
    Organization,
)
from newutils.organizations import (
    format_organization,
)
from organizations import (
    dal as orgs_dal,
)
from typing import (
    Iterable,
)


class OrganizationTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_key: Iterable[str]
    ) -> tuple[Organization, ...]:
        if any("ORG#" in orgs_id for orgs_id in organization_key):
            organization_items = await collect(
                orgs_dal.get_by_id(organization_id)
                for organization_id in organization_key
            )
            return tuple(
                format_organization(item) for item in organization_items
            )
        organization_items = await collect(
            orgs_dal.get_by_name(organization_name)
            for organization_name in organization_key
        )
        return tuple(format_organization(item) for item in organization_items)
