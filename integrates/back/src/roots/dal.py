from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    roots as roots_model,
)
from db_model.roots.types import (
    RootItem,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
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
)

# Constants
logging.config.dictConfig(LOGGING)
LOGGER: logging.Logger = logging.getLogger(__name__)


async def get_root(*, group_name: str, root_id: str) -> Optional[RootItem]:
    return await roots_model.get_root(group_name=group_name, root_id=root_id)


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    return await roots_model.get_roots(group_name=group_name)


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
