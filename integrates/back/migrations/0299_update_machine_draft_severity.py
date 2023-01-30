# pylint: disable=invalid-name
"""
Updates the severity of Machine drafts
that may have been created with that parameter empty

Execution Time:    2022-10-12 at 21:46:08 UTC
Finalization Time: 2022-10-12 at 21:47:12 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    AttackComplexity,
    AttackVector,
    AvailabilityImpact,
    ConfidentialityImpact,
    Exploitability,
    IntegrityImpact,
    PrivilegesRequired,
    RemediationLevel,
    ReportConfidence,
    SeverityScope,
    UserInteraction,
)
from db_model.findings.types import (
    Finding31Severity,
)
from decimal import (
    Decimal,
)
from findings.domain import (
    get_severity_score,
    update_severity,
)
from newutils.findings import (
    get_vulns_file,
)
from organizations.domain import (
    get_all_active_group_names,
)
import time


async def main() -> None:
    loaders = get_new_context()
    criteria = await get_vulns_file()
    groups = await get_all_active_group_names(loaders)
    groups_drafts = await loaders.group_drafts.load_many(list(groups))

    total_groups: int = len(groups)
    for idx, (group, drafts) in enumerate(zip(groups, groups_drafts)):
        print(f"Processing group {group} ({idx+1}/{total_groups})...")
        machine_drafts = [
            draft for draft in drafts if draft.state.source == Source.MACHINE
        ]
        no_severity = [
            draft
            for draft in machine_drafts
            if get_severity_score(draft.severity) == Decimal("0")
        ]
        if no_severity:
            print("\t" + f"{len(no_severity)} drafts to update:")
            print(
                "\t\t" + "\n\t\t".join([draft.title for draft in no_severity])
            )
            await collect(
                (
                    update_severity(
                        loaders,
                        draft.id,
                        Finding31Severity(
                            attack_complexity=AttackComplexity[
                                criteria[draft.title[:3]]["score"]["base"][
                                    "attack_complexity"
                                ]
                            ].value,
                            attack_vector=AttackVector[
                                criteria[draft.title[:3]]["score"]["base"][
                                    "attack_vector"
                                ]
                            ].value,
                            availability_impact=AvailabilityImpact[
                                criteria[draft.title[:3]]["score"]["base"][
                                    "availability"
                                ]
                            ].value,
                            confidentiality_impact=ConfidentialityImpact[
                                criteria[draft.title[:3]]["score"]["base"][
                                    "confidentiality"
                                ]
                            ].value,
                            exploitability=Exploitability[
                                criteria[draft.title[:3]]["score"]["temporal"][
                                    "exploit_code_maturity"
                                ]
                            ].value,
                            integrity_impact=IntegrityImpact[
                                criteria[draft.title[:3]]["score"]["base"][
                                    "integrity"
                                ]
                            ].value,
                            privileges_required=PrivilegesRequired[
                                criteria[draft.title[:3]]["score"]["base"][
                                    "privileges_required"
                                ]
                            ].value,
                            remediation_level=RemediationLevel[
                                criteria[draft.title[:3]]["score"]["temporal"][
                                    "remediation_level"
                                ]
                            ].value,
                            report_confidence=ReportConfidence[
                                criteria[draft.title[:3]]["score"]["temporal"][
                                    "report_confidence"
                                ]
                            ].value,
                            severity_scope=SeverityScope[
                                criteria[draft.title[:3]]["score"]["base"][
                                    "scope"
                                ]
                            ].value,
                            user_interaction=UserInteraction[
                                criteria[draft.title[:3]]["score"]["base"][
                                    "user_interaction"
                                ]
                            ].value,
                        ),
                    )
                    for draft in no_severity
                ),
                workers=15,
            )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
