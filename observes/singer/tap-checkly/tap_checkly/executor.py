import logging
from purity.v1 import (
    FrozenList,
)
from returns.io import (
    IO,
)
from tap_checkly import (
    streams,
)
from tap_checkly.api import (
    ApiClient,
    Credentials,
)
from tap_checkly.streams import (
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
    api = ApiClient.new(creds)

    for selection in targets:
        LOG.info("Executing stream: %s", selection)
        _stream_executor[selection](api)
    return IO(None)
