# pylint: disable=invalid-name
"""
Migrate portfolios metadata to "integrates_vms" table.

Execution Time:    2022-06-14 at 01:45:11 UTC
Finalization Time: 2022-06-14 at 01:46:19 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    portfolios as portfolios_model,
)
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

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_organization(
    *,
    loaders: Dataloaders,
    organization_name: str,
) -> None:
    org_portfolios = await loaders.organization_portfolios.load(
        organization_name
    )

    await collect(
        tuple(
            portfolios_model.update(portfolio=portfolio)
            for portfolio in org_portfolios
        ),
        workers=8,
    )

    LOGGER_CONSOLE.info(
        "Organization processed",
        extra={
            "extra": {
                "org_name": organization_name,
                "portfolios_len": len(org_portfolios),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_org_names: list[str] = []
    async for organization in orgs_domain.iterate_organizations():
        all_org_names.append(organization.name)
        await process_organization(
            loaders=loaders, organization_name=organization.name
        )

    LOGGER_CONSOLE.info(
        "All organizations", extra={"extra": {"processed": len(all_org_names)}}
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
