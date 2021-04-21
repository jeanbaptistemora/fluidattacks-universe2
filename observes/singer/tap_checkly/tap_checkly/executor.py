# Standard libraries
import logging
from typing import (
    Callable,
    Mapping,
)

# Third party libraries

# Local libraries
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


LOG = logging.getLogger(__name__)
_stream_executor: Mapping[
    SupportedStreams,
    Callable[[ApiClient], None]
] = {
    SupportedStreams.ALERT_CHS: streams.all_alerts,
    SupportedStreams.CHECKS: streams.all_checks,
    SupportedStreams.CHECK_GROUPS: streams.all_chk_groups,
    SupportedStreams.CHECK_STATUS: streams.all_chk_status,
    SupportedStreams.DASHBOARD: streams.all_dashboards,
    SupportedStreams.ENV_VARS: streams.all_env_vars,
    SupportedStreams.MAINTENACE_WINDOWS: streams.all_maint_windows,
    SupportedStreams.SNIPPETS: streams.all_snippets,
}


def stream(creds: Credentials, name: str) -> None:
    target_stream = SupportedStreams(name)
    LOG.info('Executing stream: %s', target_stream)
    client = ApiClient.new(creds)
    _stream_executor[target_stream](client)


def stream_all(creds: Credentials) -> None:
    client = ApiClient.new(creds)
    for target_stream, executor in _stream_executor.items():
        LOG.info('Executing stream: %s', target_stream)
        executor(client)
