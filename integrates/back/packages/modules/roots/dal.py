# Standard
from typing import Optional, Tuple

# Local
from dynamodb import model
from dynamodb.types import (
    GitRootCloning,
    GitRootItem,
    GitRootState,
    RootItem
)


async def get_root(
    *,
    group_name: str,
    url: str,
    branch: str
) -> Optional[RootItem]:
    return await model.get_root(
        group_name=group_name,
        url=url,
        branch=branch
    )


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    return await model.get_roots(group_name=group_name)


async def create_git_root(
    *,
    group_name: str,
    root: GitRootItem
) -> None:
    await model.create_git_root(group_name=group_name, root=root)


async def update_git_root_state(
    *,
    branch: str,
    group_name: str,
    state: GitRootState,
    url: str
) -> None:
    await model.update_git_root_state(
        branch=branch,
        group_name=group_name,
        state=state,
        url=url
    )


async def update_git_root_cloning(
    *,
    branch: str,
    cloning: GitRootCloning,
    group_name: str,
    url: str
) -> None:
    await model.update_git_root_cloning(
        branch=branch,
        cloning=cloning,
        group_name=group_name,
        url=url
    )
