from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    roots as roots_model,
)
from dynamodb import (
    model,
    operations_legacy as dynamodb_ops,
)
from dynamodb.types import (
    GitRootCloning,
    GitRootState,
    IPRootState,
    RootItem,
    URLRootState,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
    Union,
)

# Constants
logging.config.dictConfig(LOGGING)
LOGGER: logging.Logger = logging.getLogger(__name__)


async def get_root(*, group_name: str, root_id: str) -> Optional[RootItem]:
    return await roots_model.get_root(group_name=group_name, root_id=root_id)


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    return await model.get_roots(group_name=group_name)


async def update_git_root_cloning(
    *, cloning: GitRootCloning, group_name: str, root_id: str
) -> None:
    await model.update_git_root_cloning(
        cloning=cloning, group_name=group_name, root_id=root_id
    )


async def update_root_state(
    *,
    group_name: str,
    root_id: str,
    state: Union[GitRootState, IPRootState, URLRootState],
) -> None:
    await model.update_root_state(
        group_name=group_name, state=state, root_id=root_id
    )


async def get_root_vulns(*, nickname: str) -> Tuple[Dict[str, Any], ...]:
    return await dynamodb_ops.query(
        "FI_vulnerabilities",
        {
            "IndexName": "repo_index",
            "KeyConditionExpression": Key("repo_nickname").eq(nickname),
        },
    )


def _filter_open_and_accepted_undef_vulns(vuln: Dict[str, Any]) -> bool:
    return (
        vuln["historic_state"][-1]["state"] == "open"
        and vuln["historic_treatment"][-1]["treatment"] != "ACCEPTED_UNDEFINED"
        and vuln.get("historic_zero_risk", "")
        and vuln["historic_zero_risk"][-1]["status"] != "CONFIRMED"
    )


async def has_open_vulns(*, nickname: str) -> bool:
    vulns = await get_root_vulns(nickname=nickname)

    return bool(
        next(
            (
                vuln
                for vuln in vulns
                if _filter_open_and_accepted_undef_vulns(vuln)
            ),
            None,
        )
    )
