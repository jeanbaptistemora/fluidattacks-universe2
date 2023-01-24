# pylint: disable=invalid-name
# type: ignore
"""
It is not necessary to add the nickname at the beginning of
the vulnerabilities, the nickname was used to identify the origin of the
vulnerabilities, now each vulnerability has the root_id

Execution Time:
Finalization Time:
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
from db_model.roots.types import (
    GitRoot,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    VulnerabilityMetadataToUpdate,
)
from db_model.vulnerabilities.update import (
    update_metadata,
)
from organizations import (
    domain as orgs_domain,
)
import time
from typing import (
    Any,
    Coroutine,
    Tuple,
)
from vulnerabilities.domain.utils import (
    get_path_from_integrates_vulnerability,
)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = await orgs_domain.get_all_active_group_names(loaders=loaders)
    for group in groups:
        print(f"Processing group {group}")
        findings: Tuple[
            Finding, ...
        ] = await loaders.group_drafts_and_findings.load(group)
        vulns = await loaders.finding_vulnerabilities.load_many_chained(
            [fin.id for fin in findings]
        )
        vulns = tuple(
            vuln for vuln in vulns if vuln.type == VulnerabilityType.LINES
        )
        roots_dict: dict[str, GitRoot] = {
            root.id: root
            for root in (
                await loaders.root.load_many(
                    [
                        (group, vuln)
                        for vuln in {vuln.root_id for vuln in vulns}
                    ]
                )
            )
        }
        futures: list[Coroutine[Any, Any, None]] = []
        for vuln in vulns:
            if vuln.root_id not in roots_dict:
                continue
            if vuln.where.startswith(roots_dict[vuln.root_id].state.nickname):
                new_where = get_path_from_integrates_vulnerability(
                    vuln.where, vuln.type
                )[1]
                if vuln.where == new_where:
                    continue
                futures = [
                    *futures,
                    update_metadata(
                        finding_id=vuln.finding_id,
                        metadata=VulnerabilityMetadataToUpdate(
                            where=new_where
                        ),
                        vulnerability_id=vuln.id,
                    ),
                ]
        print(f"{len(futures)} vulnerabilities will be updated")
        await collect(
            futures,
            workers=15,
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
