# Standard libraries
import logging
import logging.config
from typing import (
    cast,
    List,
    Set
)

# Local libraries
from back.settings import LOGGING
from backend.domain import project as group_domain
from backend.typing import Project as ProjectType


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def update_tags(
    project_name: str,
    project_tags: ProjectType,
    tags: List[str]
) -> bool:
    if not project_tags['tag']:
        project_tags = {'tag': set(tags)}
    else:
        cast(Set[str], project_tags.get('tag')).update(tags)
    tags_added = await group_domain.update(project_name, project_tags)
    if tags_added:
        success = True
    else:
        LOGGER.error('Couldn\'t add tags', extra={'extra': locals()})
        success = False

    return success
