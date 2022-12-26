from custom_exceptions import (
    CredentialNotFound,
    InvalidParameter,
    RootAlreadyCloning,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from organizations import (
    domain as orgs_domain,
)
from roots import (
    domain as roots_domain,
)
from typing import (
    List,
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
            roots_domain.queue_sync_git_roots(
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
        InvalidParameter,
        CredentialNotFound,
        RootAlreadyCloning,
    ) as exc:
        message = str(exc)

    return QuequeResult(success, group_name, message)


async def clone_groups_roots(queue_with_vpn: bool = False) -> None:
    loaders: Dataloaders = get_new_context()
    groups = await orgs_domain.get_all_active_groups(loaders)
    machine_groups: List[str] = [
        group.name for group in groups if group.state.has_machine is True
    ]
    for group in machine_groups:
        await _queue_sync_git_roots(
            loaders=loaders,
            user_email="integrates@fluidattacks.com",
            group_name=group,
            queue_with_vpn=queue_with_vpn,
        )


async def main() -> None:
    await clone_groups_roots()
