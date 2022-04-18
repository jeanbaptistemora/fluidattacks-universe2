import logging
from tap_delighted import (
    streams,
)
from tap_delighted.api import (
    ApiClient,
)
from tap_delighted.auth import (
    Credentials,
)
from tap_delighted.streams import (
    SupportedStreams,
)
from typing import (
    Callable,
    Mapping,
)

LOG = logging.getLogger(__name__)

_stream_executor: Mapping[SupportedStreams, Callable[[ApiClient], None]] = {
    SupportedStreams.BOUNCED: streams.all_bounced,
    SupportedStreams.METRICS: streams.all_metrics,
    SupportedStreams.PEOPLE: streams.all_people,
    SupportedStreams.SURVEY_RESPONSE: streams.all_surveys,
    SupportedStreams.UNSUBSCRIBED: streams.all_unsubscribed,
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
