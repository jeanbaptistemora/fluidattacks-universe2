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
)
from fa_purity.pure_iter.transform import (
    chain,
)
from fa_singer_io.singer import (
    SingerRecord,
)
from tap_gitlab.api2.ids import (
    ProjectId,
)
from tap_gitlab.api2.members import (
    Member,
)
from tap_gitlab.singer.members.core import (
    SingerStreams,
)


def member_records(
    project: ProjectId, member: Member
) -> PureIter[SingerRecord]:
    encoded_obj: FrozenDict[str, UnfoldedJVal] = FrozenDict(
        {
            "project_id": project.str_val,
            "user_id": member.user[0].user_id,
            "username": member.user[1].username,
            "email": member.user[1].email,
            "name": member.user[1].name,
            "state": member.user[1].state,
            "created_at": member.user[1].created_at.isoformat(),
            "is_admin": member.user[1].is_admin,
            "membership_state": member.membership_state,
        }
    )
    records = (
        from_flist(
            (
                SingerRecord(
                    SingerStreams.members.value,
                    from_unfolded_dict(encoded_obj),
                    None,
                ),
            )
        ),
    )
    return chain(from_flist(records))
