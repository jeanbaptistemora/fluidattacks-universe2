# pylint: disable=invalid-name
# type: ignore
"""
Populate where, specific and commit in the vulnerability historic state

Execution Time: 2022-11-02 at 15:39:09 UTC
Finalization Time: 2022-11-02 at 18:13:50 UTC
"""
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
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
    TABLE,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb import (
    keys,
    operations,
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
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def process_state(  # pylint: disable=too-many-arguments
    vulnerability: Vulnerability,
    state: VulnerabilityState,
    commit: Optional[str],
    specific: str,
    where: str,
    is_last_state: bool,
) -> None:
    if (state.where is None and state.specific is None) or is_last_state:
        key_structure = TABLE.primary_key
        historic_entry_key = keys.build_key(
            facet=TABLE.facets["vulnerability_historic_state"],
            values={
                "id": vulnerability.id,
                "iso8601utc": state.modified_date,
            },
        )
        item = {
            "commit": commit,
            "specific": specific,
            "where": where,
        }
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=item,
            key=historic_entry_key,
            table=TABLE,
        )


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def process_vulnerability(
    loaders: Dataloaders, vulnerability: Vulnerability
) -> None:
    initial_commit = vulnerability.commit
    initial_specific = vulnerability.specific
    initial_where = vulnerability.where
    historic = await loaders.vulnerability_historic_state.load(
        vulnerability.id
    )
    for state in historic:
        if state.where is not None and state.specific is not None:
            initial_commit = state.commit
            initial_specific = state.specific
            initial_where = state.where
            break
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={
            "finding_id": vulnerability.finding_id,
            "id": vulnerability.id,
        },
    )
    key_structure = TABLE.primary_key
    item = {
        "state.commit": vulnerability.commit,
        "state.specific": vulnerability.specific,
        "state.where": vulnerability.where,
    }
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=item,
        key=primary_key,
        table=TABLE,
    )
    await process_state(
        vulnerability=vulnerability,
        state=historic[-1],
        commit=vulnerability.commit,
        specific=vulnerability.specific,
        where=vulnerability.where,
        is_last_state=True,
    )
    await collect(
        tuple(
            process_state(
                vulnerability=vulnerability,
                state=state,
                commit=initial_commit,
                specific=initial_specific,
                where=initial_where,
                is_last_state=False,
            )
            for state in historic[:-1]
        )
    )


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def get_finding_vulnerabilities(
    loaders: Dataloaders,
    finding_id: str,
) -> tuple[Vulnerability, ...]:
    vulnerabilities = await loaders.finding_vulnerabilities_all.load(
        finding_id
    )
    return vulnerabilities


async def process_group(loaders: Dataloaders, group_name: str) -> None:
    findings = await loaders.group_drafts_and_findings.load(group_name)
    vulnerabilities = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    get_finding_vulnerabilities(loaders, finding.id)
                    for finding in findings
                ),
                workers=500,
            )
        )
    )
    await collect(
        tuple(
            process_vulnerability(loaders, vulnerability)
            for vulnerability in vulnerabilities
        ),
        workers=500,
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
    LOGGER_CONSOLE.info(
        "All group names",
        extra={
            "extra": {
                "total": len(all_group_names),
            }
        },
    )
    for group_name in all_group_names:
        count += 1
        LOGGER_CONSOLE.info(
            "Group",
            extra={
                "extra": {
                    "group_name": group_name,
                    "count": count,
                }
            },
        )
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
