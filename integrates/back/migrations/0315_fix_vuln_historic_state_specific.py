# pylint: disable=invalid-name
# type: ignore
"""
Some specific are numbers or ranges instead of strings in the vulnerabilities

Execution Time: 2022-11-04 at 21:08:48 UTC
Finalization Time: 2022-11-04 at 22:05:01 UTC
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
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from decimal import (
    Decimal,
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
from newutils import (
    vulnerabilities as vulns_utils,
)
from organizations import (
    domain as orgs_domain,
)
import re
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
async def process_state(
    vulnerability: Vulnerability,
    state: VulnerabilityState,
    specific: str,
) -> None:
    if state.specific != specific:
        key_structure = TABLE.primary_key
        historic_entry_key = keys.build_key(
            facet=TABLE.facets["vulnerability_historic_state"],
            values={
                "id": vulnerability.id,
                "iso8601utc": state.modified_date,
            },
        )
        item = {
            "specific": specific,
        }
        LOGGER_CONSOLE.info(
            "Update",
            extra={
                "extra": {
                    "vulnerability": vulnerability.id,
                    "state.specific": state.specific,
                    "state.specific type": type(state.specific),
                    "item": item,
                }
            },
        )
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=item,
            key=historic_entry_key,
            table=TABLE,
        )


def _has_specific_range(
    vuln_type: VulnerabilityType, state: VulnerabilityState
) -> bool:
    if vuln_type in {VulnerabilityType.LINES, VulnerabilityType.PORTS}:
        specific_values = vulns_utils.ungroup_specific(state.specific)
    else:
        specific_values = (
            [state.specific]
            if re.match(
                r"(?P<specific>.*)\s\(.*\)(\s\[.*\])?$", state.specific
            )
            or state.source is Source.MACHINE
            else [spec for spec in state.specific.split(",") if spec]
        )
    if len(specific_values) > 1:
        return True
    return False


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def process_vulnerability(
    loaders: Dataloaders, vulnerability: Vulnerability
) -> None:
    last_specific = str(vulnerability.specific)
    historic = await loaders.vulnerability_historic_state.load(
        vulnerability.id
    )
    states_to_update = []
    for state in reversed(historic):
        if isinstance(state.specific, Decimal):
            last_specific = str(int(state.specific))
            states_to_update.append(
                process_state(
                    vulnerability=vulnerability,
                    state=state,
                    specific=last_specific,
                )
            )
        elif _has_specific_range(vuln_type=vulnerability.type, state=state):
            states_to_update.append(
                process_state(
                    vulnerability=vulnerability,
                    state=state,
                    specific=last_specific,
                )
            )
        else:
            last_specific = state.specific
    await collect(tuple(states_to_update))

    if isinstance(vulnerability.state.specific, Decimal):
        LOGGER_CONSOLE.info(
            "Is decimal",
            extra={
                "extra": {
                    "vulnerability": vulnerability.id,
                }
            },
        )
        last_specific = str(int(vulnerability.state.specific))
        primary_key = keys.build_key(
            facet=TABLE.facets["vulnerability_metadata"],
            values={
                "finding_id": vulnerability.finding_id,
                "id": vulnerability.id,
            },
        )
        key_structure = TABLE.primary_key
        item = {
            "state.specific": vulnerability.specific,
        }
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists(),
            item=item,
            key=primary_key,
            table=TABLE,
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
                workers=1000,
            )
        )
    )
    await collect(
        tuple(
            process_vulnerability(loaders, vulnerability)
            for vulnerability in vulnerabilities
        ),
        workers=1000,
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
