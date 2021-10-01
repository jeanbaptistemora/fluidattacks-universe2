from boto3.dynamodb.conditions import (
    Key,
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
    Tuple,
)

# Constants
logging.config.dictConfig(LOGGING)
LOGGER: logging.Logger = logging.getLogger(__name__)


async def get_root_vulns(*, nickname: str) -> Tuple[Dict[str, Any], ...]:
    return await dynamodb_ops.query(
        "FI_vulnerabilities",
        {
            "IndexName": "repo_index",
            "KeyConditionExpression": Key("repo_nickname").eq(nickname),
        },
    )


def is_open(vuln: Dict[str, Any]) -> bool:
    return (
        vuln["historic_state"][-1]["state"] == "open"
        and vuln.get("historic_zero_risk", [{}])[-1].get("status")
        != "CONFIRMED"
    )


async def has_open_vulns(
    *, nickname: str, loaders: Any, group_name: str
) -> bool:
    vulns = await get_root_vulns(nickname=nickname)
    draft_ids = (
        draft["id"] for draft in await loaders.group_drafts.load(group_name)
    )

    return bool(
        next(
            (
                vuln
                for vuln in vulns
                if is_open(vuln) and vuln["finding_id"] not in draft_ids
            ),
            None,
        )
    )
