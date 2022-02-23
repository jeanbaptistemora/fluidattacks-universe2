# pylint: disable=invalid-name
"""
Update skims_method in None state based on 0186_set_none_skims_method.yaml
for LINES vulnerabilities

Initially this migration ran without parallelism, but the execution time was
not acceptable. This version was then used to reduce that time. The runtime
goes from the start of the serial run to the end of the parallel one.

Execution Time:     2022-02-16 at 05:32:35 UTC
Finalization Time:  2022-02-17 at 08:20:27 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
)
from db_model.vulnerabilities.update import (
    update_metadata,
)
from fnmatch import (
    fnmatch,
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
    AsyncGenerator,
    Dict,
    Iterator,
    List,
    Tuple,
)
import yaml  # type: ignore

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

Element = Tuple[Finding, Vulnerability]
MethodDesc = Tuple[str, List[str]]
MethodDescDict = Dict[str, List[str]]
MethodMap = Dict[str, List[MethodDescDict]]


def vuln_is_machine(vuln: Vulnerability) -> bool:
    return vuln.state.source == Source.MACHINE


def vuln_is_line(vuln: Vulnerability) -> bool:
    return vuln.type == VulnerabilityType.LINES


def meth_is_none(vuln: Vulnerability) -> bool:
    return vuln.skims_method is None


async def list_vulns(loaders: Any, group: str) -> AsyncGenerator:
    raw_findings = await loaders.group_findings.load(group)

    findings = {finding.id: finding for finding in raw_findings}
    f_ids = findings.keys()

    for vuln in await loaders.finding_vulnerabilities.load_many_chained(f_ids):
        yield findings[vuln.finding_id], vuln


async def list_vulns_to_update(loaders: Any, group: str) -> AsyncGenerator:
    async for finding, vuln in list_vulns(loaders, group):
        if vuln_is_machine(vuln) and vuln_is_line(vuln) and meth_is_none(vuln):
            yield finding, vuln


def list_checks(methods: MethodMap, finding_code: str) -> Iterator[MethodDesc]:
    if finding := methods.get(finding_code):
        for check in finding:
            for name, extensions in check.items():
                yield name, extensions


def read_yaml(file_name: str) -> Dict[Any, Any]:
    with open(file_name, "r", encoding="utf8") as f:
        data = yaml.safe_load(f)
    return data


def extract_finding_code(finding: Finding) -> str:
    number, _ = finding.title.split(".", maxsplit=1)
    return f"F{number}"


async def process_group(
    loaders: Dataloaders, group: str, methods: MethodMap, progress: float
) -> None:
    total = 0
    updated = 0

    async for finding, vuln in list_vulns_to_update(loaders, group):
        total += 1
        finding_code = extract_finding_code(finding)
        for skims_method, patterns in list_checks(methods, finding_code):
            for pattern in patterns:
                if fnmatch(vuln.where, pattern):
                    updated += 1
                    await update_metadata(
                        finding_id=finding.id,
                        vulnerability_id=vuln.id,
                        metadata=VulnerabilityMetadataToUpdate(
                            skims_method=skims_method,
                        ),
                    )
                    break

    # pylint: disable=logging-fstring-interpolation
    LOGGER_CONSOLE.info(
        f"progress: {progress:%.2f}%, vulns updated: {updated}/{total}",
        extra={"extra": group},
    )


async def main() -> None:
    loaders = get_new_context()
    groups = await get_active_groups()
    n_groups = len(groups)

    methods = read_yaml("0186_set_none_skims_method.yaml")

    await collect(
        tuple(
            process_group(loaders, group, methods, count / n_groups * 100)
            for count, group in enumerate(groups[:10])
        ),
        workers=10,
    )


if __name__ == "__main__":
    print(format_time("Execution Time:    %Y-%m-%d at %H:%M:%S UTC"))
    run(main())
    print(format_time("Finalization Time: %Y-%m-%d at %H:%M:%S UTC"))
