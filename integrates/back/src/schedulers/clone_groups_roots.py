from batch import (
    roots as batch_roots,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    CredentialNotFound,
    InactiveRoot,
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
    Tuple,
)


async def clone_groups_roots() -> None:
    loaders: Dataloaders = get_new_context()
    group_roots_loader = loaders.group_roots

    groups: List[str] = await groups_domain.get_active_groups()
    groups_roots: Tuple[
        Tuple[RootItem, ...], ...
    ] = await group_roots_loader.load_many(groups)
    for group, roots in zip(groups, groups_roots):
        git_roots: GitRootItem = list(
            filter(lambda x: x.metadata.type == "Git", roots)
        )
        for git_root in git_roots:
            with suppress(InactiveRoot, CredentialNotFound):
                await batch_roots.queue_sync_git_root(
                    loaders=loaders,
                    root=git_root,
                    user_email="integrates@fluidattacks.com",
                    check_existing_jobs=False,
                    queue="spot_later",
                )
                info(f"Queued clone for root {git_root.id} in group {group}")


async def main() -> None:
    await clone_groups_roots()
