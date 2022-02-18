# pylint: disable=invalid-name
"""
Update vulnerabilities with skims_methods set on
query.get_vulnerabilities_from_syntax with correct method name based on
finding title

Execution Time:    2022-02-18 at 20:42:18 UTC
Finalization Time: 2022-02-18 at 20:58:57 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
)
from db_model.vulnerabilities.update import (
    update_metadata,
)
from groups.domain import (
    get_active_groups,
)
import logging
from settings import (
    LOGGING,
)
from time import (
    strftime as format_time,
)
from typing import (
    Any,
    Optional,
    Tuple,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

Element = Tuple[Optional[str], Vulnerability]

METHODS = [
    "query.query_f001",
    "query.query_f004",
    "query.query_f008",
    "query.query_f021",
    "query.query_f034",
    "query.query_f042",
    "query.query_f052",
    "query.query_f063",
    "query.query_f089",
    "query.query_f100",
    "query.query_f107",
    "query.query_f112",
    "query.query_f127",
    "query.query_f320",
]


def is_query_method(vuln: Vulnerability) -> bool:
    return vuln.skims_method == "query.get_vulnerabilities_from_syntax"


def get_new_skims_method(finding: Finding) -> Optional[str]:
    number, _ = finding.title.split(".", maxsplit=1)
    new_skims_method = f"query.query_f{number}"
    return new_skims_method if new_skims_method in METHODS else None


async def elements_to_update(loaders: Any, group: str) -> Tuple[Element, ...]:
    raw_findings = await loaders.group_findings.load(group)
    findings = {finding.id: finding for finding in raw_findings}
    f_ids = findings.keys()
    return tuple(
        (get_new_skims_method(findings[v.finding_id]), v)
        for v in await loaders.finding_vulnerabilities.load_many_chained(f_ids)
        if is_query_method(v)
    )


async def process_group(
    loaders: Dataloaders, group: str, progress: float
) -> None:
    # pylint: disable=logging-fstring-interpolation

    total = 0
    for new_skims_method, vuln in await elements_to_update(loaders, group):
        total += 1

        if new_skims_method:
            await update_metadata(
                finding_id=vuln.finding_id,
                vulnerability_id=vuln.id,
                metadata=VulnerabilityMetadataToUpdate(
                    skims_method=new_skims_method,
                ),
            )
        else:
            LOGGER_CONSOLE.info(
                f"check not founded: {vuln.skims_method}",
                extra={"extra": vuln.id},
            )

    LOGGER_CONSOLE.info(
        f"progress: {progress:.2f}%, vulns updated: {total}",
        extra={"extra": group},
    )


async def main() -> None:
    loaders = get_new_context()
    groups = await get_active_groups()
    n_groups = len(groups)

    await collect(
        tuple(
            process_group(loaders, group, count / n_groups * 100)
            for count, group in enumerate(groups)
        ),
        workers=10,
    )


if __name__ == "__main__":
    print(format_time("Execution Time:    %Y-%m-%d at %H:%M:%S UTC"))
    run(main())
    print(format_time("Finalization Time: %Y-%m-%d at %H:%M:%S UTC"))
