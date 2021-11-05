import logging
from purity.v1 import (
    FrozenList,
)
from returns.io import (
    IO,
)
from singer_io.singer2.emitter import (
    SingerEmitter,
)
from tap_checkly import (
    streams,
)
from tap_checkly.api2.checks import (
    checks_api_1,
)
from tap_checkly.api import (
    ApiClient,
    Credentials,
)
from tap_checkly.api.common.raw.client import (
    Client,
)
from tap_checkly.streams import (
    SupportedStreams,
)
from tap_checkly.streams.checks_rolled_up import (
    ChkRollStream,
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
    SupportedStreams.CHECK_RESULTS: streams.all_chk_results,
    SupportedStreams.CHECK_STATUS: streams.all_chk_status,
    SupportedStreams.DASHBOARD: streams.all_dashboards,
    SupportedStreams.ENV_VARS: streams.all_env_vars,
    SupportedStreams.MAINTENACE_WINDOWS: streams.all_maint_windows,
    SupportedStreams.REPORTS: streams.all_chk_reports,
    SupportedStreams.SNIPPETS: streams.all_snippets,
}
V2_ENABLED = False


def emit_streams(
    creds: Credentials, targets: FrozenList[SupportedStreams]
) -> IO[None]:
    api = ApiClient.new(creds)
    client = Client.new(creds)
    emitter = SingerEmitter()

    for selection in targets:
        LOG.info("Executing stream: %s", selection)
        if selection == SupportedStreams.CHECK_RESULTS and V2_ENABLED:
            stream = ChkRollStream(
                checks_api_1(client, 10),
                emitter,
                "check_result_rolled",
                "check_result_rolled_times",
            )
            stream.emit()
        else:
            _stream_executor[selection](api)
    return IO(None)
