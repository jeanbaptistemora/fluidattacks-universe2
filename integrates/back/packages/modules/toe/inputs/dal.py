
import logging
import logging.config
from typing import Tuple

from botocore.exceptions import ClientError

from back.settings import LOGGING
from custom_exceptions import (
    RepeatedToeInput,
    ToeInputNotFound,
    UnavailabilityError,
)
from data_containers.toe_inputs import GitRootToeInput
from dynamodb import model
from dynamodb.exceptions import ConditionalCheckFailedException
from dynamodb.types import GitRootToeInputItem


# Constants
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


def _format_git_toe_input(
    toe_input_item: GitRootToeInputItem
) -> GitRootToeInput:
    return GitRootToeInput(**toe_input_item._asdict())


def _format_git_toe_input_item(
    toe_input: GitRootToeInput
) -> GitRootToeInputItem:
    return GitRootToeInputItem(**toe_input._asdict())


async def create(root_toe_input: GitRootToeInput) -> None:
    try:
        root_toe_input_item = _format_git_toe_input_item(root_toe_input)
        await model.create_git_root_toe_input(
            root_toe_input=root_toe_input_item
        )
    except ConditionalCheckFailedException:
        raise RepeatedToeInput()


async def delete(
    entry_point: str,
    component: str,
    group_name: str
) -> None:
    try:
        await model.delete_git_root_toe_input(
            entry_point=entry_point,
            component=component,
            group_name=group_name
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
        raise UnavailabilityError() from ex


async def get_by_group(
    group_name: str
) -> Tuple[GitRootToeInput, ...]:
    try:
        toe_input_items = await model.get_toe_inputs_by_group(
            group_name=group_name
        )
        return tuple(map(_format_git_toe_input, toe_input_items))
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
        raise UnavailabilityError() from ex


async def update(root_toe_input: GitRootToeInput) -> None:
    try:
        root_toe_input_item = _format_git_toe_input_item(root_toe_input)
        await model.update_git_root_toe_input(
            root_toe_input=root_toe_input_item
        )
    except ConditionalCheckFailedException:
        raise ToeInputNotFound()
