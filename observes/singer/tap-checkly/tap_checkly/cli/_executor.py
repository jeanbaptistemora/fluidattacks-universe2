# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
    timezone,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Result,
    ResultE,
)
from fa_purity.pure_iter.factory import (
    pure_map,
)
from fa_purity.pure_iter.transform import (
    consume,
)
import logging
from tap_checkly import (
    streams,
)
from tap_checkly.api2 import (
    Credentials,
)
from tap_checkly.api import (
    ApiClient,
    Credentials as LegacyCreds,
)
from tap_checkly.streams import (
    Streams,
    SupportedStreams,
)
from typing import (
    Callable,
    Mapping,
)

LOG = logging.getLogger(__name__)
_legacy: Mapping[SupportedStreams, Callable[[ApiClient], Cmd[None]]] = {
    SupportedStreams.DASHBOARD: streams.all_dashboards,
    SupportedStreams.ENV_VARS: streams.all_env_vars,
    SupportedStreams.MAINTENACE_WINDOWS: streams.all_maint_windows,
    SupportedStreams.REPORTS: streams.all_chk_reports,
    SupportedStreams.SNIPPETS: streams.all_snippets,
}
OLD_DATE = datetime(1970, 1, 1, tzinfo=timezone.utc)
NOW = datetime.now(tz=timezone.utc)


def emit_stream(creds: Credentials, selection: SupportedStreams) -> Cmd[None]:
    _streams = Streams(creds, OLD_DATE, NOW)

    def stream_mapper(
        item: SupportedStreams,
    ) -> ResultE[Cmd[None]]:  # return type should be Cmd[None]
        if item is SupportedStreams.CHECKS:
            return Result.success(_streams.all_checks())
        if item is SupportedStreams.CHECK_GROUPS:
            return Result.success(_streams.check_groups())
        if item is SupportedStreams.CHECK_RESULTS:
            return Result.success(_streams.check_results())
        if item is SupportedStreams.ALERT_CHS:
            return Result.success(_streams.alert_chs())
        if item is SupportedStreams.CHECK_STATUS:
            return Result.success(_streams.check_status())
        return Result.failure(NotImplementedError(item), Cmd[None]).alt(
            Exception
        )

    def _execute(item: SupportedStreams) -> ResultE[Cmd[None]]:
        info = Cmd.from_cmd(lambda: LOG.info("Executing stream: %s", item))
        return stream_mapper(item).map(lambda a: info + a)

    return _execute(selection).or_else_call(
        lambda: _legacy[selection](
            ApiClient.new(LegacyCreds(creds.account, creds.api_key))
        )
    )


def emit_streams(
    creds: Credentials, targets: FrozenList[SupportedStreams]
) -> Cmd[None]:
    emissions = pure_map(lambda s: emit_stream(creds, s), targets)
    return consume(emissions)
