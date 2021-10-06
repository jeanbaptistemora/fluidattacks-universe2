# pylint: disable=invalid-name
"""
This migration aims to submit and approve the drafts created in previous steps,
in order to continue with the findings type standarization effort.

This is done after copying vulns and evidences from other findings.

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/4903

Execution Time:    2021-08-19 at 11:42:32 UTC-05
Finalization Time: 2021-08-19 at 11:42:46 UTC-05

Execution Time:    2021-08-20 at 21:24:02 UTC-05
Finalization Time: 2021-08-20 at 21:42:39 UTC-05

Execution Time:    2021-08-23 at 10:11:50 UTC-05
Finalization Time: 2021-08-23 at 11:55:16 UTC-05

Execution Time:    2021-08-23 at 14:30:07 UTC-05
Finalization Time: 2021-08-23 at 17:02:09 UTC-05

Execution Time:    2021-08-24 at 09:51:11 UTC-05
Finalization Time: 2021-08-24 at 11:24:48 UTC-05

Execution Time:    2021-08-24 at 12:24:27 UTC-05
Finalization Time: 2021-08-24 at 13:07:15 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import csv
from custom_exceptions import (
    AlreadyApproved,
    AlreadySubmitted,
    DraftWithoutVulns,
    IncompleteDraft,
    NotSubmitted,
)
from custom_types import (
    Finding as FindingType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from findings import (
    domain as findings_domain,
)
from newutils.findings import (
    get_historic_state,
)
import time
from typing import (
    Any,
    Dict,
    NamedTuple,
)

PROD: bool = True


class Context(NamedTuple):
    loaders: Any
    headers: Any


def _get_approver(finding: Dict[str, FindingType]) -> str:
    approver_email = ""
    approval_info = None
    historic_state = get_historic_state(finding)
    if historic_state:
        approval_info = list(
            filter(
                lambda state_info: state_info["state"] == "APPROVED",
                historic_state,
            )
        )
    if approval_info:
        approver_email = approval_info[-1]["analyst"]
    return approver_email


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
    print(f'   === target_draft: {target_draft["id"]}')

    old_finding_id = draft_info["finding_id"]
    finding_loader = context.finding
    old_finding = await finding_loader.load(old_finding_id)

    # Intermediate typing needed by the domain
    info_context = Context(loaders=context, headers={})

    success = False
    if PROD:
        analyst_email = old_finding["analyst"]
        try:
            success = await findings_domain.submit_draft(
                info_context, target_draft["id"], analyst_email
            )
        except (
            AlreadyApproved,
            AlreadySubmitted,
            IncompleteDraft,
        ) as ex:
            print(
                f'   --- ERROR draft {target_draft["id"]} - '
                f'"{target_draft["title"]}" NOT submitted: {str(ex)}'
            )
        if not success:
            print(
                f'   --- ERROR draft {target_draft["id"]} - '
                f'"{target_draft["title"]}" NOT submitted'
            )
            return False

        approver_email = _get_approver(old_finding)
        try:
            success = await findings_domain.approve_draft(
                info_context, target_draft["id"], approver_email
            )
        except (
            AlreadyApproved,
            DraftWithoutVulns,
            NotSubmitted,
        ) as ex:
            print(
                f'   --- ERROR draft {target_draft["id"]} - '
                f'"{target_draft["title"]}" NOT submitted: {str(ex)}'
            )
        print(
            f'   === draft {target_draft["id"]} - '
            f'"{target_draft["title"]}" approved: {success}'
        )

    return success


async def main() -> None:
    # Read file with new drafts info
    with open("0120.csv", mode="r", encoding="utf8") as f:
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
