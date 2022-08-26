from fa_purity.json.factory import (
    from_prim_dict,
)
from fa_singer_io.singer import (
    SingerRecord,
)
from tap_mandrill.api.objs.activity import (
    Activity,
)
from tap_mandrill.streams.core import (
    DataStreams,
)


def to_singer(file: Activity) -> SingerRecord:
    return SingerRecord(
        DataStreams.activity.value,
        from_prim_dict(
            {
                "date": file.date.isoformat(),
                "receiver": file.receiver,
                "sender": file.sender,
                "subject": file.subject,
                "status": file.status,
                "tags": file.tags,
                "subaccount": file.subaccount,
                "opens": file.opens,
                "clicks": file.clicks,
                "bounce": file.bounce,
            }
        ),
        None,
    )
