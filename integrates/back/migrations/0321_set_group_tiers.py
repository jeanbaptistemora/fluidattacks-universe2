# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
Set billing tier accordingly for all active groups:

1. Groups with OTHER tier and has_squad will become SQUAD
2. Groups with OTHER tier and has_machine will become MACHINE
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupTier,
)
from db_model.groups.types import (
    Group,
)
from groups import (
    domain as groups_domain,
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


async def _process_group(
    *,
    group: Group,
    progress: float,
) -> None:
    tier: GroupTier = group.state.tier
    if tier == GroupTier.FREE:
        if group.state.has_squad:
            tier = GroupTier.SQUAD
        elif group.state.has_machine:
            tier = GroupTier.MACHINE
        new_state = group.state._replace(tier=tier)
        await groups_domain.update_state(
            group_name=group.name,
            state=new_state,
            organization_id=group.organization_id,
        )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group.name,
                "group_tier": tier,
                "group_has_machine": group.state.has_machine,
                "group_has_squad": group.state.has_squad,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    active_groups: tuple[Group, ...] = await orgs_domain.get_all_active_groups(
        loaders
    )
    LOGGER_CONSOLE.info(
        "Active groups",
        extra={"extra": {"groups_len": len(active_groups)}},
    )
    await collect(
        tuple(
            _process_group(
                group=group,
                progress=count / len(active_groups),
            )
            for count, group in enumerate(active_groups)
        ),
        workers=1,
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
