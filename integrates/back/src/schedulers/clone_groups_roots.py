from aioextensions import (
    collect,
)
from batch import (
    roots as batch_roots,
)
from custom_exceptions import (
    CredentialNotFound,
    InactiveRoot,
    RootAlreadyCloned,
    RootAlreadyCloning,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.roots.types import (
    GitRootItem,
    RootItem,
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
    Tuple,
)


class QuequeResult(NamedTuple):
    root: RootItem
    success: bool
    group: str
    message: Optional[str] = None


async def _queue_sync_git_root(
    loaders: Dataloaders,
    root: GitRootItem,
    user_email: str,
    check_existing_jobs: bool = True,
    queue: str = "spot_soon",
    *,
    group_name: str,
) -> QuequeResult:
    success = False
    message: Optional[str] = None
    try:
        await (
            batch_roots.queue_sync_git_root(
                loaders,
                root,
                user_email,
                check_existing_jobs,
                queue,
            )
        )
        success = True
    except (
        InactiveRoot,
        CredentialNotFound,
        RootAlreadyCloned,
        RootAlreadyCloning,
    ) as exc:
        message = str(exc)

    return QuequeResult(root, success, group_name, message)


async def clone_groups_roots() -> None:
    loaders: Dataloaders = get_new_context()
    group_roots_loader = loaders.group_roots

    groups: List[str] = await groups_domain.get_active_groups()
    groups_roots: Tuple[
        Tuple[RootItem, ...], ...
    ] = await group_roots_loader.load_many(groups)
    for group, roots in zip(groups, groups_roots):
        futures = [
            _queue_sync_git_root(
                loaders=loaders,
                root=git_root,
                user_email="integrates@fluidattacks.com",
                check_existing_jobs=False,
                queue="spot_later",
                group_name=group,
            )
            for git_root in (
                root for root in roots if root.metadata.type == "Git"
            )
        ]

        for result in await collect(futures):
            if result.success:
                info(
                    (
                        f"Queued clone for root {result.root.id} in"
                        f" group {result.group}"
                    )
                )


async def main() -> None:
    await clone_groups_roots()
