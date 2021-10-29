# pylint: disable=invalid-name
"""
This migration adds the DELETED state to all findings, and their
vulnerabilities, that were reported by the non-security methods from Skims.

Execution Time:    2021-10-28 at 19:00:00 UTC
Finalization Time: 2021-10-29 at 16:01:15 UTC
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
    FindingStateJustification,
)
from findings import (
    domain as findings_domain,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
import time
from typing import (
    Dict,
    NamedTuple,
)


class Context(NamedTuple):
    headers: Dict[str, str]
    loaders: Dataloaders


async def main() -> None:
    context = Context(headers={}, loaders=get_new_context())
    findings_loader = context.loaders.group_findings
    groups = await groups_domain.get_active_groups()
    groups_findings = await findings_loader.load_many(groups)
    groups_findings = list(chain.from_iterable(groups_findings))

    titles_to_delete = {
        "060. Insecure exceptions",
        "061. Errors without traceability",
        "070. Inappropriate coding practices - Wildcard import",
        "073. Conditional statement without a default option",
        "109. Insecure functionality - Float currency",
    }
    machine_hacker_email = {
        "asalgado@fluidatacks.com",
        "jrestrepo@fluidattacks.com",
        "jrestrepo@kernelship.com",
        "kamado@fluidattacks.com",
    }
    findings_to_delete = list(
        filter(
            lambda x: (
                x.title in titles_to_delete
                and x.hacker_email in machine_hacker_email
            ),
            groups_findings,
        )
    )
    print(
        "[INFO] Findings to delete:\n[INFO]\t"
        + "\n[INFO]\t".join([finding.id for finding in findings_to_delete])
    )
    await collect(
        findings_domain.remove_finding(
            context,
            finding.id,
            FindingStateJustification.NOT_REQUIRED,
            "acuberos@fluidattacks.com",
        )
        for finding in findings_to_delete
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
