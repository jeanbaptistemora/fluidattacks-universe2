# pylint: disable=invalid-name
"""
Add the severity score to all findings

Execution Time:    2023-03-01 at 18:41:23 UTC
Finalization Time: 2023-03-01 at 18:44:39 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.types import (
    FindingMetadataToUpdate,
    SeverityScore,
)
from newutils import (
    cvss as cvss_utils,
)
from organizations.domain import (
    get_all_active_group_names,
)
import time


async def main() -> None:
    loaders = get_new_context()
    groups = await get_all_active_group_names(loaders)
    groups_drafts = await loaders.group_drafts_and_findings.load_many(
        list(groups)
    )

    total_groups: int = len(groups)
    for idx, (group, drafts) in enumerate(zip(groups, groups_drafts)):
        print(f"Processing group {group} ({idx+1}/{total_groups})...")
        futures = [
            findings_model.update_metadata(
                group_name=group,
                finding_id=fin.id,
                metadata=FindingMetadataToUpdate(
                    severity_score=SeverityScore(
                        base_score=cvss_utils.get_severity_base_score(
                            fin.severity
                        ),
                        temporal_score=cvss_utils.get_severity_temporal_score(
                            fin.severity
                        ),
                        cvssf=cvss_utils.get_cvssf_score(
                            cvss_utils.get_severity_temporal_score(
                                fin.severity
                            )
                        ),
                    )
                ),
            )
            for fin in drafts
            if fin.severity_score is None
        ]
        await collect(futures, workers=15)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
