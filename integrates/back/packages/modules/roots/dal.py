# Standard
import logging
import logging.config
from typing import Optional, Tuple

# Third party
from boto3.dynamodb.conditions import Key

# Local
from back.settings import LOGGING
from backend.dal.helpers import dynamodb as legacy_dynamodb
from dynamodb import model
from dynamodb.types import GitRootCloning, GitRootState, RootItem


# Constants
logging.config.dictConfig(LOGGING)
LOGGER: logging.Logger = logging.getLogger(__name__)


async def create_root(*, root: RootItem) -> None:
    await model.create_root(root=root)


async def get_root(*, group_name: str, root_id: str) -> Optional[RootItem]:
    return await model.get_root(
        group_name=group_name,
        root_id=root_id
    )


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    return await model.get_roots(group_name=group_name)


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


async def has_open_vulns(*, nickname: str) -> bool:
    vulns = await legacy_dynamodb.async_query(
        'FI_vulnerabilities',
        {
            'IndexName': 'repo_index',
            'KeyConditionExpression': Key('repo_nickname').eq(nickname),
        }
    )

    return bool(
        next(
            (
                vuln
                for vuln in vulns
                if vuln['historic_state'][-1]['state'] == 'open'
            ),
            None
        )
    )
