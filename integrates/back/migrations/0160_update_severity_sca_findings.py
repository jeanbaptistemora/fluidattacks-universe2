# pylint: disable=invalid-name
"""
This migration will update the severity correctly for the different SCA
findings according to Criteria.

Execution Time:     2021-11-23 at 21:53:58 UTC
Finalization Time:  2021-11-23 at 21:54:29 UTC
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
    Finding31Severity,
    FindingMetadataToUpdate,
)
from db_model.findings.update import (
    update_metadata,
)
from decimal import (
    Decimal,
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
    groups = await groups_domain.get_active_groups()
    findings = list(
        chain.from_iterable(
            await context.loaders.group_findings.load_many(groups)
        )
    )
    f011_findings = list(filter(lambda x: x.title.startswith("011"), findings))
    f393_findings = list(filter(lambda x: x.title.startswith("393"), findings))
    f011_metadata = FindingMetadataToUpdate(
        severity=Finding31Severity(
            attack_complexity=Decimal("0.77"),
            attack_vector=Decimal("0.85"),
            availability_impact=Decimal("0.22"),
            confidentiality_impact=Decimal("0.22"),
            exploitability=Decimal("0.94"),
            integrity_impact=Decimal("0.22"),
            privileges_required=Decimal("0.62"),
            remediation_level=Decimal("0.95"),
            report_confidence=Decimal("1.00"),
            user_interaction=Decimal("0.85"),
        )
    )
    f393_metadata = FindingMetadataToUpdate(
        severity=Finding31Severity(
            attack_complexity=Decimal("0.44"),
            attack_vector=Decimal("0.85"),
            availability_impact=Decimal("0.22"),
            confidentiality_impact=Decimal("0.22"),
            exploitability=Decimal("0.94"),
            integrity_impact=Decimal("0.22"),
            privileges_required=Decimal("0.62"),
            remediation_level=Decimal("0.95"),
            report_confidence=Decimal("1.00"),
            user_interaction=Decimal("0.85"),
        )
    )
    print(f"{len(f011_findings) + len(f393_findings)} findings to update:")
    print("F011 findings:")
    print("\t" + "\n\t".join([finding.id for finding in f011_findings]))
    print("F393 findings:")
    print("\t" + "\n\t".join([finding.id for finding in f393_findings]))
    await collect(
        update_metadata(
            group_name=finding.group_name,
            finding_id=finding.id,
            metadata=f011_metadata,
        )
        for finding in f011_findings
    )
    await collect(
        update_metadata(
            group_name=finding.group_name,
            finding_id=finding.id,
            metadata=f393_metadata,
        )
        for finding in f393_findings
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
