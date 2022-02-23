# pylint: disable=invalid-name
"""
Set missing developer and skims_technique for INPUTS vulnerabilities with
skims_method set.

Execution Time:    2022-02-23 at 14:29:47 UTC
Finalization Time: 2022-02-23 at 15:13:41 UTC
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
    Dict,
    Tuple,
)
import yaml  # type: ignore

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

Element = Tuple[Finding, Vulnerability]
MethodMap = Dict[Any, Any]


def read_yaml(file_name: str) -> Dict[Any, Any]:
    with open(file_name, "r", encoding="utf8") as f:
        data = yaml.safe_load(f)
    return data


def vuln_is_machine(vuln: Vulnerability) -> bool:
    return vuln.state.source == Source.MACHINE


def vuln_is_input(vuln: Vulnerability) -> bool:
    return vuln.type == VulnerabilityType.INPUTS


def meth_is_set(vuln: Vulnerability) -> bool:
    return vuln.skims_method is not None


async def vulns_to_update(
    loaders: Any, group: str
) -> Tuple[Vulnerability, ...]:
    raw_findings = await loaders.group_findings.load(group)
    f_ids = (finding.id for finding in raw_findings)
    return tuple(
        v
        for v in await loaders.finding_vulnerabilities.load_many_chained(f_ids)
        if vuln_is_machine(v) and vuln_is_input(v) and meth_is_set(v)
    )


async def process_group(
    loaders: Dataloaders, group: str, methods: MethodMap, progress: float
) -> None:
    # pylint: disable=logging-fstring-interpolation

    total = 0
    for vuln in await vulns_to_update(loaders, group):
        total += 1

        if method := methods.get(vuln.skims_method):
            await update_metadata(
                finding_id=vuln.finding_id,
                vulnerability_id=vuln.id,
                metadata=VulnerabilityMetadataToUpdate(
                    developer=method["developer"],
                    skims_technique=method["technique"],
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

    methods = read_yaml("0195_update_developer_and_technique_in_inputs.yaml")

    await collect(
        tuple(
            process_group(loaders, group, methods, count / n_groups * 100)
            for count, group in enumerate(groups)
        ),
        workers=10,
    )


if __name__ == "__main__":
    print(format_time("Execution Time:    %Y-%m-%d at %H:%M:%S UTC"))
    run(main())
    print(format_time("Finalization Time: %Y-%m-%d at %H:%M:%S UTC"))
