from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenList,
    JsonObj,
    Result,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    pure_map,
)
from fa_purity.result.transform import (
    all_ok,
)
from tap_checkly.api._utils import (
    ExtendedUnfolder,
)
from tap_checkly.objs import (
    AlertChannelId,
    ChannelSubscription,
    CheckGroup,
    CheckGroupId,
    CheckGroupObj,
    IndexedObj,
)


def _decode_ch_sub(raw: JsonObj) -> ResultE[ChannelSubscription]:
    unfolder = ExtendedUnfolder(raw)
    return unfolder.require_primitive("activated", bool).bind(
        lambda activated: unfolder.require_primitive("alertChannelId", int)
        .map(AlertChannelId)
        .map(lambda channel: ChannelSubscription(activated, channel))
    )


def _decode_subs(raw: JsonObj) -> ResultE[FrozenList[ChannelSubscription]]:
    unfolder = ExtendedUnfolder(raw)
    return (
        unfolder.get("alertChannelSubscriptions")
        .map(
            lambda j: Unfolder(j)
            .to_list()
            .alt(Exception)
            .bind(
                lambda l: all_ok(
                    pure_map(
                        lambda i: Unfolder(i)
                        .to_json()
                        .alt(Exception)
                        .bind(_decode_ch_sub),
                        l,
                    ).to_list()
                )
            )
        )
        .value_or(Result.success(tuple()))
    )


def _decode_locations(raw: JsonObj) -> ResultE[FrozenList[str]]:
    unfolder = ExtendedUnfolder(raw)
    return (
        unfolder.get("locations")
        .map(lambda j: Unfolder(j).to_list_of(str).alt(Exception))
        .value_or(Result.success(tuple()))
    )


@dataclass(frozen=True)
class CheckGroupDecoder:
    raw: JsonObj

    def decode_check(self) -> ResultE[CheckGroup]:
        unfolder = ExtendedUnfolder(self.raw)
        return unfolder.require_primitive("activated", bool).bind(
            lambda activated: unfolder.require_primitive(
                "concurrency", int
            ).bind(
                lambda concurrency: unfolder.require_primitive(
                    "name", str
                ).bind(
                    lambda name: _decode_subs(self.raw).bind(
                        lambda alert_channels: unfolder.require_datetime(
                            "created_at"
                        ).bind(
                            lambda created_at: unfolder.opt_datetime(
                                "updated_at"
                            ).bind(
                                lambda updated_at: unfolder.require_primitive(
                                    "doubleCheck", bool
                                ).bind(
                                    lambda double_check: _decode_locations(
                                        self.raw
                                    ).bind(
                                        lambda locations: unfolder.require_primitive(
                                            "muted", bool
                                        ).bind(
                                            lambda muted: unfolder.maybe_primitive(
                                                "runtimeId", str
                                            ).bind(
                                                lambda runtime_id: unfolder.require_primitive(
                                                    "useGlobalAlertSettings",
                                                    bool,
                                                ).map(
                                                    lambda use_global_alert_settings: CheckGroup(
                                                        activated,
                                                        concurrency,
                                                        name,
                                                        alert_channels,
                                                        created_at,
                                                        updated_at,
                                                        double_check,
                                                        locations,
                                                        muted,
                                                        runtime_id,
                                                        use_global_alert_settings,
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

    def decode_id(self) -> ResultE[CheckGroupId]:
        unfolder = ExtendedUnfolder(self.raw)
        return unfolder.require_primitive("id", int).map(CheckGroupId)

    def decode_obj(self) -> ResultE[CheckGroupObj]:
        return self.decode_id().bind(
            lambda cid: self.decode_check().map(lambda c: IndexedObj(cid, c))
        )
