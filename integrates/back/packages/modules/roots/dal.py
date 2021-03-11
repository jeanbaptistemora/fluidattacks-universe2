# Standard
from typing import Optional, Tuple

# Local
from dynamodb import model
from dynamodb.types import (
    RootHistoricCloning,
    RootHistoricState,
    RootItem,
    RootMetadata
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


async def create_root(
    *,
    cloning: RootHistoricCloning,
    group_name: str,
    metadata: RootMetadata,
    state: RootHistoricState
) -> None:
    await model.create_root(
        cloning=cloning,
        group_name=group_name,
        metadata=metadata,
        state=state
    )


async def update_root_state(
    *,
    branch: str,
    group_name: str,
    state: RootHistoricState,
    url: str
) -> None:
    await model.update_root_state(
        branch=branch,
        group_name=group_name,
        state=state,
        url=url
    )


async def update_root_cloning(
    *,
    branch: str,
    cloning: RootHistoricCloning,
    group_name: str,
    url: str
) -> None:
    await model.update_root_cloning(
        branch=branch,
        cloning=cloning,
        group_name=group_name,
        url=url
    )
