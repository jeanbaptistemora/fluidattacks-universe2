# Standard libraries
import logging
import logging.config
from typing import Tuple

# Third party libraries
from botocore.exceptions import ClientError

# Local libraries
from back.settings import LOGGING
from backend.exceptions import (
    UnavailabilityError,
)
from dynamodb import model
from dynamodb.types import GitRootToeLines

# Constants
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


async def get_by_root(
    *,
    group_name: str,
    root_id: str
) -> Tuple[GitRootToeLines, ...]:
    try:
        return await model.get_toe_lines_by_root(
            group_name=group_name,
            root_id=root_id
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
        raise UnavailabilityError() from ex


async def update(root_toe_lines: GitRootToeLines) -> None:
    try:
        await model.update_git_root_toe_lines(
            root_toe_lines=root_toe_lines
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
        raise UnavailabilityError() from ex
