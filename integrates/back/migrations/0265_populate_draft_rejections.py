# pylint: disable=invalid-name
"""
Populate the draft rejection info in the respective finding historic states

Execution Time:
Finalization Time:

Execution Time:
Finalization Time:
"""
import csv
from datetime import (
    datetime,
)
from db_model.findings.enums import (
    DraftRejectionReason,
)
import logging
import logging.config
from newutils import (
    datetime as date_utils,
)
from settings import (
    LOGGING,
)
from typing import (
    NamedTuple,
)

# Constants
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


class RejectionHelper(NamedTuple):
    finding_id: str
    raw_date: datetime
    reasons: set[DraftRejectionReason]
    rejected_by: str
    submitted_by: str


def resolve_reviewer(raw_reviewer: str, date: datetime) -> str:
    old_reviewer: str = "oprado@fluidattacks.com"
    new_reviewer: str = "emorales@fluidattacks.com"
    cut_off_date: datetime = date_utils.get_from_str("13/05/2022", "%d/%m/%Y")
    known_reviewers: dict[str, str] = {
        "E": new_reviewer,
        "G": "",
        "J": "jmartinez@fluidattacks.com",
        "O": old_reviewer,
    }
    if raw_reviewer in known_reviewers:
        return known_reviewers[raw_reviewer]
    return old_reviewer if date < cut_off_date else new_reviewer


def parse_reasons(
    raw_reasons: list[str],
) -> set[DraftRejectionReason]:
    reasons: list[DraftRejectionReason] = [
        DraftRejectionReason.WRITING,
        DraftRejectionReason.EVIDENCE,
        DraftRejectionReason.SCORING,
        DraftRejectionReason.CONSISTENCY,
        DraftRejectionReason.OMISSION,
        DraftRejectionReason.NAMING,
        DraftRejectionReason.OTHER,
    ]
    return {
        reasons[position]
        for position, raw_reason in enumerate(raw_reasons)
        if raw_reason
    }


def parse_rejection_file() -> dict[str, list[RejectionHelper]]:
    rejection_info: dict[str, list[RejectionHelper]] = {}

    with open(
        file="rejection_file.csv", mode="r", encoding="utf-8"
    ) as rejection_file:
        rows = (tuple(line) for line in csv.reader(rejection_file))
        for (
            raw_reviewer,
            finding_id,
            submitted_by,
            raw_date,
            *reasons,
        ) in rows:
            rejection_date = date_utils.get_from_str(raw_date, "%d/%m/%Y")
            rejection_info.setdefault(finding_id, []).append(
                RejectionHelper(
                    finding_id=finding_id,
                    raw_date=rejection_date,
                    reasons=parse_reasons(reasons),
                    submitted_by=submitted_by,
                    rejected_by=resolve_reviewer(raw_reviewer, rejection_date),
                )
            )

    return rejection_info
