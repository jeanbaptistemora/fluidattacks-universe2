# type: ignore

# pylint: disable=invalid-name
"""
Add creation date to all urls

Execution Time:    2022-04-27 at 17:26:25 UTC
Finalization Time: 2022-04-27 at 17:42:45 UTC
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
from groups.dal import (  # pylint: disable=import-error
    get_all as get_all_groups,
)
import logging
import logging.config
from roots.domain import (
    add_root_environment_url,
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
            environment_urls = await loaders.root_environment_urls.load(
                root.id
            )
            await collect(
                [
                    add_root_environment_url(
                        loaders=loaders,
                        group_name=group,
                        root_id=root.id,
                        url=env_url.url,
                        url_type="URL",
                        user_email="",
                    )
                    for env_url in environment_urls
                    if env_url.created_at is None
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
