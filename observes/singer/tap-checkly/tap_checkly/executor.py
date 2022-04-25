from fa_purity.cmd import (
    unsafe_unwrap,
)
from fa_purity.stream.transform import (
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
from tap_checkly import (
    streams,
)
from tap_checkly.api2 import (
    Credentials,
)
from tap_checkly.api2.checks import (
    ChecksClient,
)
from tap_checkly.api import (
    ApiClient,
    Credentials as LegacyCreds,
)
from tap_checkly.streams import (
    encoder,
    SupportedStreams,
)
from typing import (
    Callable,
    Mapping,
)

LOG = logging.getLogger(__name__)
_stream_executor: Mapping[SupportedStreams, Callable[[ApiClient], None]] = {
    SupportedStreams.ALERT_CHS: streams.all_alerts,
    SupportedStreams.CHECKS: streams.all_checks,
    SupportedStreams.CHECK_GROUPS: streams.all_chk_groups,
    SupportedStreams.CHECK_RESULTS: (lambda _: None),
    SupportedStreams.CHECK_STATUS: streams.all_chk_status,
    SupportedStreams.DASHBOARD: streams.all_dashboards,
    SupportedStreams.ENV_VARS: streams.all_env_vars,
    SupportedStreams.MAINTENACE_WINDOWS: streams.all_maint_windows,
    SupportedStreams.REPORTS: streams.all_chk_reports,
    SupportedStreams.SNIPPETS: streams.all_snippets,
}


def emit_streams(
    creds: Credentials, targets: FrozenList[SupportedStreams]
) -> IO[None]:
    api = ApiClient.new(LegacyCreds(creds.account, creds.api_key))
    chks_client = ChecksClient.new(creds, 100)
    for selection in targets:
        LOG.info("Executing stream: %s", selection)
        if selection is SupportedStreams.CHECK_RESULTS:
            emissions = (
                streams.all_check_results(chks_client)
                .map(encoder.encode_result)
                .map(
                    lambda j: SingerRecord(
                        SupportedStreams.CHECK_RESULTS.value, j, None
                    )
                )
                .map(lambda s: emitter.emit(sys.stdout, s))
            )
            unsafe_unwrap(consume(emissions))
        _stream_executor[selection](api)
    return IO(None)
