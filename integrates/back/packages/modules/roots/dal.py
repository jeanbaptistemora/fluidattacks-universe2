# Standard
import logging
import logging.config
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)

# Third party
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Local
from back.settings import LOGGING
from backend.dal.helpers import dynamodb
from backend.exceptions import UnavailabilityError
from dynamodb import model
from dynamodb.types import GitRootCloning, GitRootState, RootItem


# Constants
logging.config.dictConfig(LOGGING)
LOGGER: logging.Logger = logging.getLogger(__name__)
LEGACY_TABLE_NAME: str = 'fi_roots'


async def create_root(*, group_name: str, root: RootItem) -> None:
    await model.create_root(group_name=group_name, root=root)


async def get_root(
    *,
    group_name: str,
    root_id: str
) -> Optional[RootItem]:
    return await model.get_root(
        group_name=group_name,
        root_id=root_id
    )


async def get_root_by_id_legacy(
    group_name: str,
    root_id: str
) -> Optional[Dict[str, Any]]:
    results = await dynamodb.async_query(
        LEGACY_TABLE_NAME,
        {
            'IndexName': 'roots_index',
            'KeyConditionExpression': (
                Key('sk').eq(root_id) & Key('pk').eq(f'GROUP#{group_name}')
            )
        }
    )
    return results[0] if results else None


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    return await model.get_roots(group_name=group_name)


async def get_roots_by_group_legacy(
    group_name: str
) -> Tuple[Dict[str, Any], ...]:
    return tuple(await dynamodb.async_query(
        LEGACY_TABLE_NAME,
        {
            'KeyConditionExpression': (
                Key('pk').eq(f'GROUP#{group_name}') &
                Key('sk').begins_with('ROOT#')
            ),
        }
    ))


async def update_legacy(
    group_name: str,
    root_id: str,
    root_attributes: Dict[str, Any]
) -> None:
    try:
        set_actions: Tuple[str, ...] = tuple(
            f'#{attribute} = :{attribute}'
            for attribute in root_attributes
        )
        attribute_names: Dict[str, str] = {
            f'#{attribute}': attribute
            for attribute in root_attributes
        }
        attribute_values: Dict[str, Any] = {
            f':{attribute}': root_attributes[attribute]
            for attribute in root_attributes
        }

        await dynamodb.async_update_item(
            LEGACY_TABLE_NAME,
            {
                'ExpressionAttributeNames': attribute_names,
                'ExpressionAttributeValues': attribute_values,
                'Key': {
                    'pk': f'GROUP#{group_name}',
                    'sk': root_id
                },
                'UpdateExpression': f'SET {",".join(set_actions)}',
            }
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
        raise UnavailabilityError() from ex


async def update_git_root_cloning(
    *,
    cloning: GitRootCloning,
    group_name: str,
    root_id: str
) -> None:
    await model.update_git_root_cloning(
        cloning=cloning,
        group_name=group_name,
        root_id=root_id
    )


async def update_git_root_state(
    *,
    group_name: str,
    root_id: str,
    state: GitRootState
) -> None:
    await model.update_git_root_state(
        group_name=group_name,
        state=state,
        root_id=root_id
    )
