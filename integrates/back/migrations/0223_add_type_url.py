# pylint: disable=invalid-name
"""
Add creation type to all urls

Execution Time:    2022-06-07 at 11:43:38 UTCUTC
Finalization Time: 2022-06-07 at 12:00:00 UTCUTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRoot,
)
import logging
import logging.config
from organizations.domain import (
    get_all_active_group_names,
)
from roots.domain import (
    add_git_environment_url,
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
    loaders = get_new_context()
    groups = await get_all_active_group_names(loaders)
    loaders = get_new_context()
    groups_roots_dict = dict(
        await collect([_get_group_roots(loaders, group) for group in groups])
    )
    for group, roots in groups_roots_dict.items():
        for root in roots:
            if not isinstance(root, GitRoot):
                continue
            environment_urls: list[
                GitEnvironmentUrl
            ] = await loaders.git_environment_urls.load(root.id)
            await collect(
                [
                    add_git_environment_url(
                        loaders,
                        group,
                        root.id,
                        env_url.url,
                        url_type="URL",
                    )
                    for env_url in environment_urls
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
