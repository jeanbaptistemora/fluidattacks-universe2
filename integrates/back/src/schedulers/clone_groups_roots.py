# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from batch_dispatch import (
    clone_roots,
)
from custom_exceptions import (
    CredentialNotFound,
    InactiveRoot,
    RootAlreadyCloning,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    NamedTuple,
    Optional,
)


class QuequeResult(NamedTuple):
    success: bool
    group: str
    message: Optional[str] = None


async def _queue_sync_git_roots(
    *,
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    queue_with_vpn: bool = False,
) -> QuequeResult:
    success = False
    message: Optional[str] = None
    try:
        result = await (
            clone_roots.queue_sync_git_roots(
                loaders=loaders,
                user_email=user_email,
                group_name=group_name,
                queue_with_vpn=queue_with_vpn,
                from_scheduler=True,
            )
        )
        if result is not None:
            success = result.success
    except (
        InactiveRoot,
        CredentialNotFound,
        RootAlreadyCloning,
    ) as exc:
        message = str(exc)

    return QuequeResult(success, group_name, message)


async def clone_groups_roots(queue_with_vpn: bool = False) -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)
    active_groups = await orgs_domain.get_all_active_groups(loaders)
    group_names = tuple(
        group.name for group in active_groups if group.state.has_machine
    )
    for group in group_names:
        await _queue_sync_git_roots(
            loaders=loaders,
            user_email="integrates@fluidattacks.com",
            group_name=group,
            queue_with_vpn=queue_with_vpn,
        )


async def main() -> None:
    await clone_groups_roots()
