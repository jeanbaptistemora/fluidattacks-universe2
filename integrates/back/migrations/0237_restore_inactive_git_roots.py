# type: ignore

# pylint: disable=invalid-name
"""
Restore the inactive git root state to the date before adding the credentials

Execution Time:    2022-06-30 at 21:03:39 UTC
Finalization Time: 2022-06-30 at 21:08:13 UTC
"""
from aioextensions import (
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    TABLE,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRootState,
    Root,
    RootState,
)
from dynamodb import (
    keys,
    operations,
)
import json
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    cast,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def restore_inactive_root(
    group_name: str,
    root_id: str,
    prev_state: GitRootState,
    current_state: GitRootState,
) -> None:
    state_item = json.loads(json.dumps(prev_state))
    root_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name, "uuid": root_id},
    )
    root_item = {"state": state_item}
    await operations.update_item(
        item=root_item,
        key=root_key,
        table=TABLE,
    )

    # delete historic
    historic_key = keys.build_key(
        facet=TABLE.facets["git_root_historic_state"],
        values={
            "uuid": root_id,
            "iso8601utc": current_state.modified_date,
        },
    )
    await operations.delete_item(key=historic_key, table=TABLE)


async def process_organization(
    loaders: Dataloaders,
    organization_name: str,
) -> None:
    organization_roots = cast(
        tuple[Root, ...],
        await loaders.organization_roots.load(organization_name),
    )
    for organization_root in organization_roots:
        if (
            organization_root.state.status == RootStatus.INACTIVE
            and organization_root.state.modified_by
            == "aaguirre@fluidattacks.com"
        ):
            historic_state: tuple[
                RootState, ...
            ] = await loaders.root_historic_states.load(organization_root.id)
            sorted_historic = sorted(
                historic_state,
                key=lambda state: datetime.fromisoformat(state.modified_date),
                reverse=True,
            )
            prev_state_date = sorted_historic[1].modified_date
            prev_state_modified_by = sorted_historic[1].modified_by
            prev_state = organization_root.state._replace(
                modified_date=prev_state_date,
                modified_by=prev_state_modified_by,
            )
            if sorted_historic[1].status == RootStatus.INACTIVE:
                await restore_inactive_root(
                    group_name=organization_root.group_name,
                    root_id=organization_root.id,
                    prev_state=prev_state,
                    current_state=organization_root.state,
                )


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    count = 0
    async for _, org_name, _ in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        count += 1
        print(count, org_name)
        await process_organization(loaders, org_name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
