# pylint: disable=invalid-name
"""
Remove vulnerabilities without finding

Execution Time:    2022-09-15 at 21:25:05 UTC
Finalization Time: 2022-09-15 at 21:56:48 UTC
"""
from aioextensions import (
    collect,
    run,
)
from botocore.exceptions import (
    ConnectTimeoutError,
    ReadTimeoutError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    retry_on_exceptions,
)
from itertools import (
    chain,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def process_vulnerability(vulnerability: Vulnerability) -> None:
    print(
        "vulnerability to remove", vulnerability.finding_id, vulnerability.id
    )
    await vulns_model.remove(vulnerability_id=vulnerability.id)


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def get_root_vulnerabilities(
    loaders: Dataloaders,
    root_id: str,
) -> list[Vulnerability]:
    return await loaders.root_vulnerabilities.load(root_id)


async def process_group(loaders: Dataloaders, group_name: str) -> None:
    findings: tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    finding_ids = {finding.id for finding in findings}
    roots = await loaders.group_roots.load(group_name)
    vulnerabilities = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    get_root_vulnerabilities(loaders, root.id)
                    for root in roots
                ),
                workers=300,
            )
        )
    )
    await collect(
        tuple(
            process_vulnerability(vulnerability)
            for vulnerability in vulnerabilities
            if vulnerability.finding_id not in finding_ids
        )
    )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "all_vulnerabilities": len(vulnerabilities),
            }
        },
    )


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    all_organization_ids = {"ORG#unknown"}
    async for organization in orgs_domain.iterate_organizations():
        all_organization_ids.add(organization.id)

    all_group_names = sorted(
        tuple(
            chain.from_iterable(
                await collect(
                    tuple(
                        orgs_domain.get_group_names(loaders, organization_id)
                        for organization_id in all_organization_ids
                    ),
                    workers=100,
                )
            )
        )
    )
    count = 0
    print("all_group_names", len(all_group_names))
    for group_name in all_group_names:
        count += 1
        print("group", group_name, count)
        await process_group(loaders, group_name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
