from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from newutils.organization_access import (
    format_organization_access,
)
from organizations.dal import (
    get_organization_access,
)
from typing import (
    Iterable,
)


class OrganizationAcessTypedLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, keys: Iterable[tuple[str, str]]
    ) -> tuple[OrganizationAccess, ...]:
        items = await collect(
            tuple(
                (
                    get_organization_access(
                        organization_id=org_id, user_email=email
                    )
                    for org_id, email in keys
                )
            )
        )
        return tuple(format_organization_access(item=item) for item in items)
