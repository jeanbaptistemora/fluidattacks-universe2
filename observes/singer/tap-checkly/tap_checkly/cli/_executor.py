from . import (
    _streams,
)
from ._streams._objs import (
    SupportedStreams,
)
from datetime import (
    datetime,
    timezone,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from fa_purity.stream.transform import (
    chain,
    consume,
)
from fa_singer_io.singer import (
    emitter,
    SingerRecord,
)
import logging
from purity.v1 import (
    FrozenList,
)
from returns.io import (
    IO,
)
import sys
from tap_checkly.api2 import (
    Credentials,
)
from tap_checkly.api2.alert_channels import (
    AlertChannelsClient,
)
from tap_checkly.api2.checks import (
    ChecksClient,
)
from tap_checkly.api2.id_objs import (
    IndexedObj,
)
from tap_checkly.api import (
    ApiClient,
    Credentials as LegacyCreds,
)
from tap_checkly.singer.alert_channels.records import (
    alert_ch_records,
)
from tap_checkly.singer.checks.results.records import (
    encode_result,
)
from typing import (
    Callable,
    Mapping,
)

LOG = logging.getLogger(__name__)
_stream_executor: Mapping[
    SupportedStreams, Callable[[ApiClient], Cmd[None]]
] = {
    SupportedStreams.CHECKS: _streams.all_checks,
    SupportedStreams.CHECK_GROUPS: _streams.all_chk_groups,
    SupportedStreams.CHECK_STATUS: _streams.all_chk_status,
    SupportedStreams.DASHBOARD: _streams.all_dashboards,
    SupportedStreams.ENV_VARS: _streams.all_env_vars,
    SupportedStreams.MAINTENACE_WINDOWS: _streams.all_maint_windows,
    SupportedStreams.REPORTS: _streams.all_chk_reports,
    SupportedStreams.SNIPPETS: _streams.all_snippets,
}
OLD_DATE = datetime(1970, 1, 1, tzinfo=timezone.utc)
NOW = datetime.now(tz=timezone.utc)


def _emit_stream(
    records: Stream[SingerRecord],
) -> Cmd[None]:
    emissions = records.map(lambda s: emitter.emit(sys.stdout, s))
    return consume(emissions)


def emit_streams(
    creds: Credentials, targets: FrozenList[SupportedStreams]
) -> None:
    api = ApiClient.new(LegacyCreds(creds.account, creds.api_key))
    chks_client = ChecksClient.new(creds, 100, OLD_DATE, NOW)
    for selection in targets:
        LOG.info("Executing stream: %s", selection)
        if selection is SupportedStreams.CHECK_RESULTS:
            action = _emit_stream(
                chks_client.list_ids()
                .bind(
                    lambda c: chks_client.list_check_results(c).map(
                        lambda r: IndexedObj(c, r)
                    )
                )
                .map(encode_result)
                .transform(chain),
            )
            unsafe_unwrap(action)
        elif selection is SupportedStreams.ALERT_CHS:
            action = _emit_stream(
                AlertChannelsClient.new(creds, 100)
                .list_all()
                .map(alert_ch_records)
                .transform(chain),
            )
            unsafe_unwrap(action)
        else:
            action = _stream_executor[selection](api)
            unsafe_unwrap(action)
    return None
