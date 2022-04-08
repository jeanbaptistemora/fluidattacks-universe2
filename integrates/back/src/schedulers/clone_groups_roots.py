from batch.actions import (
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
from groups import (
    domain as groups_domain,
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
    queue: str = "spot_soon",
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
                queue=queue,
                group_name=group_name,
                queue_with_vpn=queue_with_vpn,
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

    groups: List[str] = await groups_domain.get_active_groups()

    for group in groups:
        await _queue_sync_git_roots(
            loaders=loaders,
            user_email="integrates@fluidattacks.com",
            queue="spot_later",
            group_name=group,
            queue_with_vpn=queue_with_vpn,
        )


async def main() -> None:
    await clone_groups_roots()
