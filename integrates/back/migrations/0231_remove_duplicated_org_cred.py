# type: ignore

# pylint: disable=invalid-name
"""
Remove duplicated organization credentials

Execution Time:    2022-06-14 at 17:52:21 UTC
Finalization Time: 2022-06-14 at 17:53:40 UTC
"""
from aioextensions import (
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    credentials as credentials_model,
)
from db_model.credentials.types import (
    Credential,
)
import itertools
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_organization(
    loaders: Dataloaders,
    organization_id: str,
) -> None:
    org_new_credentials: tuple[
        Credential, ...
    ] = await loaders.organization_credentials_new.load(organization_id)
    for _, group in itertools.groupby(
        org_new_credentials, lambda x: x.state.name
    ):
        grouped_credentials = list(group)
        if len(grouped_credentials) > 1:
            for credential in grouped_credentials[1:]:
                await credentials_model.remove_new(
                    credential_id=credential.id,
                    organization_id=organization_id,
                )


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    count = 0
    async for org_id, org_name, _ in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        count += 1
        print(count, org_name)
        await process_organization(loaders, org_id)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
