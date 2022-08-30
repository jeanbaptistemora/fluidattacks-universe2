# pylint: disable=invalid-name
"""
Populate the draft rejection info in the respective finding historic states

Execution Time:
Finalization Time:

Execution Time:
Finalization Time:
"""
from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from collections import (
    deque,
)
import csv
from custom_exceptions import (
    FindingNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    TABLE,
)
from db_model.findings.enums import (
    DraftRejectionReason,
    FindingStateStatus,
)
from db_model.findings.types import (
    DraftRejection,
    Finding,
    FindingState,
)
from db_model.findings.utils import (
    format_state_item,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import logging
import logging.config
from newutils import (
    datetime as date_utils,
)
from organizations.domain import (
    get_all_active_group_names,
)
from settings import (
    LOGGING,
)
import time
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
        "G": "gmoran@fluidattacks.com",
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


def parse_rejection_file() -> dict[str, deque[RejectionHelper]]:
    rejection_info: dict[str, deque[RejectionHelper]] = {}

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
            rejection_info.setdefault(finding_id, deque()).append(
                RejectionHelper(
                    finding_id=finding_id,
                    raw_date=rejection_date,
                    reasons=parse_reasons(reasons),
                    submitted_by=submitted_by,
                    rejected_by=resolve_reviewer(raw_reviewer, rejection_date),
                )
            )

    return rejection_info


async def update_finding_state(
    old_state: FindingState, helper: RejectionHelper
) -> None:
    """Adds the rejection data to a copy of the old state and sends it to
    dynamo"""
    rejection: DraftRejection = DraftRejection(
        other="The draft did not fulfill the required standards"
        if DraftRejectionReason.OTHER in helper.reasons
        else "",
        reasons=helper.reasons,
        rejected_by=helper.rejected_by,
        rejection_date=old_state.modified_date,
        submitted_by=helper.submitted_by,
    )
    new_state: FindingState = FindingState(
        modified_by=old_state.modified_by,
        modified_date=old_state.modified_date,
        rejection=rejection,
        source=old_state.source,
        status=old_state.status,
    )

    key_structure = TABLE.primary_key
    new_state_item = format_state_item(new_state)
    state_key = keys.build_key(
        facet=TABLE.facets["finding_historic_state"],
        values={
            "id": helper.finding_id,
            "iso8601utc": old_state.modified_date,
        },
    )

    try:
        await operations.update_item(
            condition_expression=Attr(key_structure.partition_key).exists()
            & Attr("state.status").eq(FindingStateStatus.REJECTED.value)
            & Attr("state.modified_date").eq(old_state.modified_date)
            & Attr("state.rejection").not_exists(),
            item=new_state_item,
            key=state_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise FindingNotFound() from ex


def filter_states_by_day(
    queue: deque[FindingState], current_date: str
) -> tuple[FindingState, ...]:
    filtered_list: list[FindingState] = []
    while (
        len(queue) > 0
        and queue[-1].modified_date.split("T")[0] == current_date.split("T")[0]
    ):
        filtered_list.append(queue.pop())
    return tuple(filtered_list)


def filter_rejections_by_day(
    queue: deque[RejectionHelper], current_date: str
) -> tuple[RejectionHelper, ...]:
    filtered_list: list[RejectionHelper] = []
    while (
        len(queue) > 0
        and date_utils.get_as_utc_iso_format(queue[0].raw_date).split("T")[0]
        == current_date.split("T")[0]
    ):
        filtered_list.append(queue.popleft())
    return tuple(filtered_list)


async def handle_day_step(
    old_states: tuple[FindingState, ...],
    rejections: tuple[RejectionHelper, ...],
) -> None:
    for old_state, rejection_helper in zip(old_states, rejections):
        await update_finding_state(old_state, rejection_helper)


async def handle_finding(
    loaders: Dataloaders,
    finding_id: str,
    rejections: deque[RejectionHelper],
    group_name: str,
) -> None:

    historic_states: tuple[
        FindingState, ...
    ] = await loaders.finding_historic_state.load(finding_id)
    rejected_states: deque[FindingState] = deque(
        filter(
            lambda state: state.status == FindingStateStatus.REJECTED,
            historic_states,
        )
    )

    try:
        assert len(rejected_states) <= len(rejections)
    except AssertionError:
        LOGGER.error("Failed on %s", group_name)
        LOGGER.error("Rejected states %s", len(rejected_states))
        LOGGER.error("Rejections %s", len(rejections))
        raise


async def handle_group(
    loaders: Dataloaders,
    group_name: str,
    rejections: dict[str, deque[RejectionHelper]],
) -> None:
    all_findings: tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)

    await collect(
        tuple(
            handle_finding(
                loaders=loaders,
                finding_id=finding.id,
                rejections=rejections[finding.id],
                group_name=group_name,
            )
            for finding in all_findings
            if finding.id in rejections
        ),
        workers=20,
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    rejections = parse_rejection_file()
    all_group_names: tuple[str] = await get_all_active_group_names(loaders)
    await collect(
        tuple(
            handle_group(
                loaders=loaders,
                group_name=group_name,
                rejections=rejections,
            )
            for group_name in all_group_names
        ),
        workers=5,
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
