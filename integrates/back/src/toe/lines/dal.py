from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    RepeatedToeLines,
    ToeLinesNotFound,
    UnavailabilityError,
)
from data_containers.toe_lines import (
    GitRootToeLines,
)
from dynamodb import (
    model,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from dynamodb.types import (
    GitRootToeLinesItem,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    Tuple,
)

# Constants
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


def _format_git_toe_lines(
    toe_lines_item: GitRootToeLinesItem,
) -> GitRootToeLines:
    return GitRootToeLines(**toe_lines_item._asdict())


def _format_git_toe_lines_item(
    toe_lines: GitRootToeLines,
) -> GitRootToeLinesItem:
    return GitRootToeLinesItem(**toe_lines._asdict())


async def add(root_toe_lines: GitRootToeLines) -> None:
    try:
        root_toe_lines_item = _format_git_toe_lines_item(root_toe_lines)
        await model.add_git_root_toe_lines(root_toe_lines=root_toe_lines_item)
    except ConditionalCheckFailedException:
        raise RepeatedToeLines()


async def remove(filename: str, group_name: str, root_id: str) -> None:
    try:
        await model.remove_git_root_toe_lines(
            filename=filename, group_name=group_name, root_id=root_id
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
        raise UnavailabilityError() from ex


async def get_by_group(group_name: str) -> Tuple[GitRootToeLines, ...]:
    try:
        toe_lines_items = await model.get_toe_lines_by_group(
            group_name=group_name
        )
        return tuple(map(_format_git_toe_lines, toe_lines_items))
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
        raise UnavailabilityError() from ex


async def get_by_root(
    group_name: str, root_id: str
) -> Tuple[GitRootToeLines, ...]:
    try:
        toe_lines_items = await model.get_toe_lines_by_root(
            group_name=group_name, root_id=root_id
        )
        return tuple(map(_format_git_toe_lines, toe_lines_items))
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
        raise UnavailabilityError() from ex


async def update(root_toe_lines: GitRootToeLines) -> None:
    try:
        root_toe_lines_item = _format_git_toe_lines_item(root_toe_lines)
        await model.update_git_root_toe_lines(
            root_toe_lines=root_toe_lines_item
        )
    except ConditionalCheckFailedException:
        raise ToeLinesNotFound()
