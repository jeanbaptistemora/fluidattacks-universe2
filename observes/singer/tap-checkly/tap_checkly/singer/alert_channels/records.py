from ._core import (
    SingerStreams,
)
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
from tap_checkly.api2.alert_channels import (
    AlertChannelObj,
)


def alert_ch_records(obj: AlertChannelObj) -> PureIter[SingerRecord]:
    encoded_obj: FrozenDict[str, UnfoldedJVal] = FrozenDict(
        {
            "alert_ch_id": obj.id_obj.id_int,
            "alert_type": obj.obj.alert_type,
            "send_recovery": obj.obj.send_recovery,
            "send_failure": obj.obj.send_failure,
            "send_degraded": obj.obj.send_degraded,
            "ssl_expiry": obj.obj.ssl_expiry,
            "ssl_expiry_threshold": obj.obj.ssl_expiry_threshold,
            "created_at": obj.obj.created_at.isoformat(),
            "updated_at": obj.obj.updated_at.map(
                lambda d: d.isoformat()
            ).value_or(None),
        }
    )
    records = (
        from_flist(
            (
                SingerRecord(
                    SingerStreams.alert_channels.value,
                    from_unfolded_dict(encoded_obj),
                    None,
                ),
            )
        ),
    )
    return chain(from_flist(records))
