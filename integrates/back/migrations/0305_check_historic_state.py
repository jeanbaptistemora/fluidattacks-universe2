# pylint: disable=invalid-name
"""
Exploratory search of missing historic state attributes by using format_state

First Execution Time:    2022-10-26 at 02:45:23 UTC
First Finalization Time: 2022-10-26 at 02:54:37 UTC
Second Execution Time:    2022-10-26 at 16:43:16 UTC
Second Finalization Time: 2022-10-26 at 16:51:45 UTC
"""
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.group_access.get import (
    GroupStakeholdersAccessLoader,
)
from db_model.roots.types import (
    GitRoot,
    IPRoot,
    Root,
    URLRoot,
)
from db_model.roots.utils import (
    format_git_state,
    format_ip_state,
    format_url_state,
)
from dynamodb import (
    keys,
    operations,
)
from itertools import (
    chain,
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
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _get_historic_state(*, root_id: str) -> tuple[Any, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_historic_state"],
        values={"uuid": root_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(
            TABLE.facets["git_root_historic_state"],
            TABLE.facets["ip_root_historic_state"],
            TABLE.facets["url_root_historic_state"],
        ),
        table=TABLE,
    )

    return tuple(response.items)


async def process_root_ip(root: Root, historic: tuple[Any, ...]) -> None:
    for index, state in enumerate(historic):
        try:
            format_ip_state(state)
        except IndexError as exc:
            LOGGER_CONSOLE.info(
                "Working on ip root",
                extra={
                    "extra": {
                        "ex": exc,
                        "index": index,
                        "group_name": root.group_name,
                        "historic": historic,
                        "root_id": root.id,
                    }
                },
            )


async def process_root_url(root: Root, historic: tuple[Any, ...]) -> None:
    for index, state in enumerate(historic):
        try:
            format_url_state(state)
        except IndexError as exc:
            LOGGER_CONSOLE.info(
                "Working on url root",
                extra={
                    "extra": {
                        "ex": exc,
                        "index": index,
                        "group_name": root.group_name,
                        "historic": historic,
                        "root_id": root.id,
                    }
                },
            )


async def process_root(*, root: Root) -> None:  # noqa: MC0001
    historic: tuple[Any, ...] = await _get_historic_state(root_id=root.id)

    if isinstance(root, GitRoot):
        for index, state in enumerate(historic):
            try:
                format_git_state(state)
            except IndexError as exc:
                LOGGER_CONSOLE.info(
                    "Working on git root",
                    extra={
                        "extra": {
                            "ex": exc,
                            "index": index,
                            "group_name": root.group_name,
                            "historic": historic,
                            "root_id": root.id,
                        }
                    },
                )

    if isinstance(root, IPRoot):
        await process_root_ip(root, historic)

    if isinstance(root, URLRoot):
        await process_root_url(root, historic)


async def _process_group(*, loaders: Dataloaders, group_name: str) -> None:
    historic: tuple[GroupStakeholdersAccessLoader, ...] = tuple()
    try:
        historic = await loaders.group_historic_state.load(group_name)
    except IndexError as exc:
        LOGGER_CONSOLE.info(
            "Error loading group historic_state",
            extra={
                "extra": {
                    "ex": exc,
                    "group_name": group_name,
                    "historic": historic,
                }
            },
        )


async def process_group(
    *, loaders: Dataloaders, group_name: str, progress: float
) -> None:
    LOGGER_CONSOLE.info(
        "Working on group",
        extra={
            "extra": {
                "group_name": group_name,
                "progress": round(progress, 2),
            }
        },
    )
    await _process_group(loaders=loaders, group_name=group_name)
    roots = await loaders.group_roots.load(group_name)
    await collect(
        tuple(process_root(root=root) for root in roots),
        workers=2,
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_organization_ids = {"ORG#unknown"}
    async for organization in orgs_domain.iterate_organizations():
        all_organization_ids.add(organization.id)

    all_group_names: list[str] = list(
        sorted(
            tuple(
                chain.from_iterable(
                    await collect(
                        tuple(
                            orgs_domain.get_group_names(
                                loaders, organization_id
                            )
                            for organization_id in all_organization_ids
                        ),
                        workers=32,
                    )
                )
            )
        )
    )
    LOGGER_CONSOLE.info(
        "All groups",
        extra={"extra": {"groups_len": len(all_group_names)}},
    )
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / len(all_group_names),
            )
            for count, group_name in enumerate(all_group_names)
        ),
        workers=2,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
