# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    FrozenDict,
    PureIter,
    UnfoldedJVal,
)
from fa_purity.json.factory import (
    from_unfolded_dict,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    pure_map,
)
from fa_purity.pure_iter.transform import (
    chain,
)
from fa_singer_io.singer import (
    SingerRecord,
)
from tap_gitlab.api2.ids import (
    IssueId,
    UserId,
)
from tap_gitlab.api2.issues import (
    IssueObj,
)
from tap_gitlab.singer.issues.core import (
    SingerStreams,
)


def _encode_assignee(
    issue: IssueId, assignee: UserId
) -> FrozenDict[str, UnfoldedJVal]:
    return FrozenDict(
        {
            "issue_id": str(issue.global_id),
            "assignee": assignee.user_id,
        }
    )


def _encode_label(issue: IssueId, label: str) -> FrozenDict[str, UnfoldedJVal]:
    return FrozenDict(
        {
            "issue_id": str(issue.global_id),
            "label": label,
        }
    )


def issue_records(issue_obj: IssueObj) -> PureIter[SingerRecord]:
    issue = issue_obj[1]
    encoded_issue: FrozenDict[str, UnfoldedJVal] = FrozenDict(
        {
            "id": str(issue_obj[0].global_id),
            "iid": issue_obj[0].internal_id,
            "title": issue.title,
            "state": issue.state,
            "issue_type": issue.issue_type.value,
            "confidential": issue.confidential,
            "discussion_locked": issue.discussion_locked.value_or(None),
            "author_id": issue.author.user_id,
            "up_votes": issue.up_votes,
            "down_votes": issue.down_votes,
            "merge_requests_count": issue.merge_requests_count,
            "description": issue.description.value_or(None),
            "milestone_id": issue.milestone.map(
                lambda m: m.global_id
            ).value_or(None),
            "milestone_iid": issue.milestone.map(
                lambda m: m.internal_id
            ).value_or(None),
            "due_date": issue.due_date.map(lambda d: d.isoformat()).value_or(
                None
            ),
            "epic_id": issue.epic.map(lambda e: e.global_id).value_or(None),
            "epic_iid": issue.epic.map(lambda e: e.internal_id).value_or(None),
            "weight": issue.weight.value_or(None),
            "created_at": issue.created_at.isoformat(),
            "updated_at": issue.updated_at.map(
                lambda d: d.isoformat()
            ).value_or(None),
            "closed_at": issue.closed_at.map(lambda d: d.isoformat()).value_or(
                None
            ),
            "closed_by": issue.closed_by.map(lambda u: u.user_id).value_or(
                None
            ),
            "health_status": issue.health_status.value_or(None),
        }
    )
    assignees_records = pure_map(
        lambda a: _encode_assignee(issue_obj[0], a), issue.assignees
    ).map(
        lambda d: SingerRecord(
            SingerStreams.issue_assignees.value, from_unfolded_dict(d), None
        )
    )
    labels_records = pure_map(
        lambda l: _encode_label(issue_obj[0], l), issue.labels
    ).map(
        lambda d: SingerRecord(
            SingerStreams.issue_labels.value, from_unfolded_dict(d), None
        )
    )
    records = (
        from_flist(
            (
                SingerRecord(
                    SingerStreams.issue.value,
                    from_unfolded_dict(encoded_issue),
                    None,
                ),
            )
        ),
        assignees_records,
        labels_records,
    )
    return chain(from_flist(records))
