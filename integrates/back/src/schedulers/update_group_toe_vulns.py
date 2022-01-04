from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils import (
    bugsnag as bugsnag_utils,
)
from settings import (
    LOGGING,
)
from typing import (
    Optional,
    Set,
    Tuple,
)

logging.config.dictConfig(LOGGING)
LOGGER_CONSOLE = logging.getLogger("console")

bugsnag_utils.start_scheduler_session()


async def main() -> None:
    groups = await groups_domain.get_alive_group_names()
    loaders = get_new_context()

    for group in sorted(groups, reverse=True):
        LOGGER_CONSOLE.info("group", extra={"extra": {"id": group}})

        findings: Tuple[Finding, ...]
        findings = await loaders.group_findings.load(group)

        root_ids_and_wheres: Set[Tuple[Optional[str], str]] = set()

        for finding in findings:
            LOGGER_CONSOLE.info(
                "  finding", extra={"extra": {"id": finding.id}}
            )

            vulns: Tuple[Vulnerability]
            vulns = await loaders.finding_vulns_nzr_typed.load(finding.id)

            for vuln in vulns:
                if vuln.state.status is VulnerabilityStateStatus.OPEN:
                    root_ids_and_wheres.add((vuln.root_id, vuln.where))
