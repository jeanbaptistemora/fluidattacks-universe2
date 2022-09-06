import logging
from tap_bugsnag import (
    streams,
)
from tap_bugsnag.api import (
    ApiClient,
    Credentials,
)
from tap_bugsnag.streams import (
    SupportedStreams,
)
from typing import (
    Callable,
    Mapping,
)

LOG = logging.getLogger(__name__)
_stream_executor: Mapping[SupportedStreams, Callable[[ApiClient], None]] = {
    SupportedStreams.COLLABORATORS: streams.all_collaborators,
    SupportedStreams.ERRORS: streams.all_errors,
    SupportedStreams.EVENTS: streams.all_events,
    SupportedStreams.EVENT_FIELDS: streams.all_event_fields,
    SupportedStreams.ORGS: streams.all_orgs,
    SupportedStreams.PIVOTS: streams.all_pivots,
    SupportedStreams.PROJECTS: streams.all_projects,
    SupportedStreams.RELEASES: streams.all_releases,
    SupportedStreams.STABILITY_TREND: streams.all_trends,
}


def stream(creds: Credentials, name: str) -> None:
    target_stream = SupportedStreams(name)
    LOG.info("Executing stream: %s", target_stream)
    client = ApiClient.new(creds)
    _stream_executor[target_stream](client)


def stream_all(creds: Credentials) -> None:
    client = ApiClient.new(creds)
    for target_stream, executor in _stream_executor.items():
        LOG.info("Executing stream: %s", target_stream)
        executor(client)
