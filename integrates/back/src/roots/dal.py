from boto3.dynamodb.conditions import (
    Key,
)
from db_model.findings.types import (
    Finding,
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


async def get_root_vulns(
    *, loaders: Any, group_name: str, nickname: str
) -> Tuple[Dict[str, Any], ...]:
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    finding_ids = {finding.id for finding in findings}
    vulns = await dynamodb_ops.query(
        "FI_vulnerabilities",
        {
            "IndexName": "repo_index",
            "KeyConditionExpression": Key("repo_nickname").eq(nickname),
        },
    )
    return tuple(vuln for vuln in vulns if vuln["finding_id"] in finding_ids)
