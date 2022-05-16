# pylint: disable=invalid-name
"""
Remove useless comments on findings

Execution Time:    UTCUTC
Finalization Time: UTCUTC
Currently working on this
"""
from aioextensions import (
    run,
)
from comments import (
    domain as comments_domain,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
import logging
import logging.config
from organizations.domain import (
    get_all_active_group_names,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
TABLE_NAME: str = "FI_findings"


async def main() -> None:  # noqa: MC0001
    loaders = get_new_context()
    groups = sorted(await get_all_active_group_names(loaders=loaders))

    for group in groups:
        findings: Tuple[Finding, ...] = await loaders.group_findings.load(
            group
        )

    for finding_id in [finding.id for finding in findings]:
        comments = await comments_domain.get("comment", finding_id)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
