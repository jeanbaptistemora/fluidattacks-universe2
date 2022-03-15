from batch import (
    roots as batch_roots,
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
from schedulers.common import (
    info,
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
) -> QuequeResult:
    success = False
    message: Optional[str] = None
    try:
        result = await (
            batch_roots.queue_sync_git_roots(
                loaders=loaders,
                user_email=user_email,
                queue=queue,
                group_name=group_name,
            )
        )
        success = result.success
    except (
        InactiveRoot,
        CredentialNotFound,
        RootAlreadyCloning,
    ) as exc:
        message = str(exc)

    return QuequeResult(success, group_name, message)


async def clone_groups_roots() -> None:
    loaders: Dataloaders = get_new_context()

    groups: List[str] = sorted(
        await groups_domain.get_active_groups(), reverse=True
    )

    for group in groups:
        result = await _queue_sync_git_roots(
            loaders=loaders,
            user_email="integrates@fluidattacks.com",
            queue="spot_later",
            group_name=group,
        )
        if result.success:
            info(f"Queued clone for group {result.group}")
        else:
            info(f"No queued clone for group {result.group}, {result.message}")


async def main() -> None:
    await clone_groups_roots()
