# Standard libraries
import functools
import logging
import logging.config
from typing import (
    Dict,
    Set
)

# Third party libraries
from botocore.exceptions import ClientError

# Local libraries
from back.settings import LOGGING
from backend.dal.helpers import dynamodb
from backend.typing import (
    ToeLines,
    DalToeLines
)

# Constants
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = 'FI_toe_lines'
MAPPING: Dict[str, Dict[str, str]] = {
    'pk': {
        'prefix': 'ROOT#',
        'name': 'root_id'
    },
    'sk': {
        'prefix': 'FILENAME#',
        'name': 'filename'
    }
}
FIELD_NAMES: Set[str] = functools.reduce(
    lambda names, item: {*names, item['name']},
    MAPPING.values(),
    set()
)


def _map_keys_to_dal(toe_lines: ToeLines) -> DalToeLines:
    """
    Map domain keys to its DynamoDB representation
    """
    mapped_toe_lines = {
        key: getattr(toe_lines, key)
        for key in toe_lines._fields
        if key not in FIELD_NAMES
    }
    mapped_toe_lines.update({
        key: (
            f'{MAPPING[key]["prefix"]}'
            f'{getattr(toe_lines, MAPPING[key]["name"])}'
        )
        for key in MAPPING
    })
    dal_toe_lines = DalToeLines(**mapped_toe_lines)

    return dal_toe_lines


async def create(toe_lines: ToeLines) -> bool:
    """Create a toe lines"""
    success = False
    try:
        dal_toe_lines = _map_keys_to_dal(toe_lines)
        success = await dynamodb.async_put_item(
            TABLE_NAME, dal_toe_lines._asdict()
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})

    return success
