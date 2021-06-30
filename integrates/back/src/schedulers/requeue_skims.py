from context import (
    PRODUCT_API_TOKEN,
)
from dataloaders import (
    get_new_context,
)
from groups.domain import (
    get_active_groups,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import skims_sdk
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger("console")


def _info(*args: Any, extra: Any = None) -> None:
    LOGGER.info(*args, extra=dict(extra=extra))


def _error(*args: Any, extra: Any = None) -> None:
    LOGGER.error(*args, extra=dict(extra=extra))


async def skims_queue(
    finding_title: str,
    group_name: str,
) -> None:
    skims_queue_kwargs = dict(
        finding_code=None,
        finding_title=finding_title,
        group=group_name,
        urgent=True,
        product_api_token=PRODUCT_API_TOKEN,
    )

    if await skims_sdk.queue(**skims_queue_kwargs):
        _info("Successfully queued skims", extra=skims_queue_kwargs)
    else:
        _error("Could not queue a skims execution", extra=skims_queue_kwargs)


async def main() -> None:
    groups = await get_active_groups()
    context = get_new_context()

    for group in sorted(groups):

        for finding in await context.group_findings.load(group):
            finding_id: str = finding["finding_id"]
            finding_title: str = finding["finding"]

            _info("%s-%s", group, finding_id)
            for vuln in await context.finding_vulns.load(finding_id):
                vuln_source: str = vuln["source"]
                vuln_hv = vuln.get("historic_verification", [])

                if (
                    vuln_source == "skims"
                    and vuln_hv
                    and vuln_hv[-1].get("status") == "REQUESTED"
                ):
                    await skims_queue(
                        finding_title=finding_title,
                        group_name=group,
                    )
                    # Skims will analyze the entire finding
                    # so we can early abort this loop
                    break
