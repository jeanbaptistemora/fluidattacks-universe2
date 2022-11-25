from aioextensions import (
    collect,
)
from azure_repositories.domain import (
    update_organization_unreliable,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.organizations.get import (
    get_all_organizations,
)
from db_model.organizations.types import (
    Organization,
)
import logging
import logging.config
from operator import (
    attrgetter,
)
from organizations.domain import (
    get_all_active_group_names,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    organizations: tuple[Organization, ...] = await get_all_organizations()
    all_group_names: set[str] = set(await get_all_active_group_names(loaders))
    organizations_sorted_by_name = sorted(
        organizations, key=attrgetter("name")
    )
    len_gorganizations_sorted_by_name = len(organizations_sorted_by_name)

    await collect(
        tuple(
            update_organization_unreliable(
                organization=organization,
                loaders=loaders,
                progress=count / len_gorganizations_sorted_by_name,
                all_group_names=all_group_names,
            )
            for count, organization in enumerate(organizations_sorted_by_name)
        ),
        workers=1,
    )
