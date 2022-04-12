# pylint: disable=invalid-name
"""
This migration reverts a root deactivation by restoring vuln states.

Execution Time:    2022-04-12 at 00:10:03 UTC
Finalization Time: 2022-04-12 at 00:10:17 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.enums import (
    StateRemovalJustification,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from dynamodb import (
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
import logging
from settings import (
    LOGGING,
)
import simplejson as json  # type: ignore
import time
from typing import (
    List,
    Tuple,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


async def process_vuln(loaders: Dataloaders, vuln: Vulnerability) -> None:
    LOGGER.info("Processing vuln", extra={"extra": {"vuln_id": vuln.id}})
    historic_state: Tuple[
        VulnerabilityState, ...
    ] = await loaders.vulnerability_historic_state.load(vuln.id)
    previous_state = historic_state[-2]

    await operations.update_item(
        condition_expression=(
            Attr("pk").exists()
            & Attr("state.modified_date").eq(vuln.state.modified_date)
        ),
        item={"state": json.loads(json.dumps(previous_state))},
        key=PrimaryKey(
            partition_key=f"VULN#{vuln.id}",
            sort_key=f"FIN#{vuln.finding_id}",
        ),
        table=TABLE,
    )
    await operations.delete_item(
        key=PrimaryKey(
            partition_key=f"VULN#{vuln.id}",
            sort_key=f"STATE#{vuln.state.modified_date}",
        ),
        table=TABLE,
    )

    LOGGER.info("Vuln processed", extra={"extra": {"vuln_id": vuln.id}})


async def process_root(loaders: Dataloaders, root_id: str) -> None:
    vulns: Tuple[Vulnerability, ...] = await loaders.root_vulnerabilities.load(
        root_id
    )
    LOGGER.info(
        "Processing root",
        extra={"extra": {"root_id": root_id, "vulns": len(vulns)}},
    )

    await collect(
        tuple(
            process_vuln(loaders, vuln)
            for vuln in vulns
            if vuln.state.status == VulnerabilityStateStatus.CLOSED
            and vuln.state.justification == StateRemovalJustification.EXCLUSION
        ),
        workers=100,
    )

    LOGGER.info(
        "Root processed",
        extra={"extra": {"root_id": root_id, "vulns": len(vulns)}},
    )


async def main() -> None:
    roots: List[str] = []  # Masked
    loaders: Dataloaders = get_new_context()

    for root in roots:
        await process_root(loaders, root)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
