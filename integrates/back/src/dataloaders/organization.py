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
        self, organization_ids: Iterable[str]
    ) -> tuple[Organization, ...]:
        organization_items = await collect(
            orgs_dal.get_by_id(organization_id)
            for organization_id in organization_ids
        )
        return tuple(format_organization(item) for item in organization_items)
