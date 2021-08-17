# pylint: disable=invalid-name
"""
This migration aims to copy the evidences for new drafts,
in order to continue with the findings standarization.

Evidences will be copied to drafts created in the previous migration.

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/4903

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
import csv
from custom_types import (
    Finding as FindingType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from findings import (
    dal as findings_dal,
    domain as findings_domain,
)
from starlette.datastructures import (
    UploadFile,
)
import time
from typing import (
    Dict,
    List,
)

PROD: bool = False


async def move_evidence(
    file: Dict[str, str],
    group_name: str,
    target_draft_id: str,
    from_finding_id: str,
) -> bool:
    success = False
    # Download evidence
    filepath = await findings_domain.download_evidence_file(
        group_name, from_finding_id, file["file_url"]
    )
    # Upload evidence to target draft
    with open(filepath, "rb") as f:
        uploaded_file = UploadFile(f.name, f)
        success = await findings_domain.update_evidence(
            target_draft_id, file["name"], uploaded_file
        )
        if success:
            # Update description
            description = file.get("description", "")
            success = await findings_domain.update_evidence_description(
                target_draft_id, file["name"], description
            )

    if success:
        print(f'   === evidence {file["name"]} - {filepath} MOVED ok')
    else:
        print(f'   --- ERROR evidence "{file["name"]}"')

    return success


async def process_draft(
    context: Dataloaders,
    draft_info: Dict[str, str],
) -> bool:
    group_drafts_loader = context.group_drafts
    group_drafts = await group_drafts_loader.load(draft_info["group_name"])
    group_drafts_titles = [finding["title"] for finding in group_drafts]

    if draft_info["new_draft"] not in group_drafts_titles:
        print(f'   --- ERROR draft "{draft_info["new_draft"]}" NOT found')
        return False
    target_draft = next(
        finding
        for finding in group_drafts
        if finding["title"] == draft_info["new_draft"]
    )

    # Get origin finding with the evidence we want
    finding: FindingType = await findings_dal.get_finding(
        draft_info["finding_id"]
    )

    if not finding:
        print(
            f'   --- ERROR finding "{draft_info["finding_id"]}" NOT found!!!'
        )

    finding_files: List[Dict[str, str]] = finding.get("files", [])
    success = all(
        await collect(
            move_evidence(
                file,
                draft_info["group_name"],
                target_draft["id"],
                finding["finding_id"],
            )
            for file in finding_files
        )
    )

    return success


async def main() -> None:
    # Read file with new drafts info
    with open("0121_dummy.csv", mode="r") as f:
        reader = csv.reader(f)
        new_drafts_info = [
            {
                "group_name": row[0],
                "new_draft": row[1],
                "finding_id": row[2],
            }
            for row in reader
            if row[0] != "group_name"
        ]
    print(f"    === new drafts: {len(new_drafts_info)}")
    print(f"    === sample: {new_drafts_info[:1]}")

    context: Dataloaders = get_new_context()
    success = all(
        await collect(
            [
                process_draft(context, new_draft)
                for new_draft in new_drafts_info
            ]
        )
    )

    print(f"   === success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
