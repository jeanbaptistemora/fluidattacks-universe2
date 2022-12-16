# pylint: disable=invalid-name
"""
Fix offset-naive datetime in vuln latest state.
This means some ISO8601dates are missing the timezone info
and datetime comparison could fail with offset-aware dates.

Execution Time:    2022-11-04 at 19:10:13 UTC
Finalization Time: 2022-11-04 at 19:25:14 UTC
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
    VulnerabilityState,
)
from decorators import (
    retry_on_exceptions,
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

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
ISO8601_TZ_SUFFIX: str = "+00:00"


def _filter_vulns_by_datetime_str(
    vulns: tuple[Vulnerability, ...]
) -> tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulns
        if not vuln.state.modified_date.endswith(  # type: ignore
            ISO8601_TZ_SUFFIX,
        )
    )


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def _process_vuln(
    loaders: Dataloaders,
    group_name: str,
    vuln: Vulnerability,
) -> None:
    historic_state: tuple[
        VulnerabilityState, ...
    ] = await loaders.vulnerability_historic_state.load(vuln.id)
    fixed_historic_state = tuple(
        entry
        if entry.modified_date.endswith(  # type: ignore
            ISO8601_TZ_SUFFIX,
        )
        else entry._replace(
            modified_date=f"{entry.modified_date}"  # type: ignore
            f"{ISO8601_TZ_SUFFIX}",
        )
        for entry in historic_state
    )
    await vulns_model.update_historic(
        current_value=vuln, historic=fixed_historic_state
    )
    LOGGER_CONSOLE.info(
        "Vuln processed",
        extra={
            "extra": {
                "group_name": group_name,
                "vulnerability": vuln.id,
            }
        },
    )


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
    sleep_seconds=3,
)
async def _process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    group_vulns: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load_many_chained(
        list(finding.id for finding in findings)
    )
    vulns_to_fix = _filter_vulns_by_datetime_str(group_vulns)
    if not vulns_to_fix:
        return

    await collect(
        tuple(
            _process_vuln(loaders=loaders, group_name=group_name, vuln=vuln)
            for vuln in vulns_to_fix
        ),
        workers=16,
    )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "findings": len(findings),
                "vulnerabilities": len(group_vulns),
                "vulnerabilities_fixed": len(vulns_to_fix),
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await orgs_domain.get_all_active_group_names(loaders))
    LOGGER_CONSOLE.info(
        "Groups to process",
        extra={"extra": {"groups_len": len(group_names)}},
    )
    await collect(
        tuple(
            _process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / len(group_names),
            )
            for count, group_name in enumerate(group_names)
        ),
        workers=8,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
