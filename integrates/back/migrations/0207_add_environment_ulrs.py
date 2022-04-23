# pylint: disable=invalid-name
"""
Populate the zero risk index in vulnerabilities.

Execution Time:    2022-04-23 at 12:55:04 UTC
Finalization Time: 2022-04-23 at 13:15:38 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.types import (
    GitRootItem,
)
from groups.dal import (
    get_all as get_all_groups,
)
import logging
import logging.config
from roots.domain import (
    add_environment_url,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    Any,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _get_group_roots(dataloaders: Any, group: str) -> Tuple[str, Any]:
    return (group, await dataloaders.group_roots.load(group))


async def main() -> None:
    groups = await get_all_groups(data_attr="project_name")
    loaders = get_new_context()
    groups_roots_dict = dict(
        await collect(
            [
                _get_group_roots(loaders, group["project_name"])
                for group in groups
            ]
        )
    )
    for group, roots in groups_roots_dict.items():
        for root in roots:
            if not isinstance(root, GitRootItem):
                continue

            await collect(
                [
                    add_environment_url(loaders, group, root.id, url)
                    for url in root.state.environment_urls
                ]
            )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
