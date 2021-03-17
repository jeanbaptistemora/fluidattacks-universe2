# Standard libraries
from typing import (
    Callable,
    IO,
    Mapping,
    Optional,
)

# Third party libraries

# Local libraries
from tap_mailchimp import (
    api,
    streams
)
from tap_mailchimp.api import (
    ApiClient,
)
from tap_mailchimp.auth import (
    Credentials,
)
from tap_mailchimp.streams import (
    SupportedStreams
)


_stream_executor: Mapping[
    SupportedStreams,
    Callable[[ApiClient, Optional[IO[str]]], None]
] = {
    SupportedStreams.AUDIENCES: streams.all_audiences,
    SupportedStreams.ABUSE_REPORTS: streams.all_abuse_reports,
    SupportedStreams.RECENT_ACTIVITY: streams.recent_activity,
    SupportedStreams.TOP_CLIENTS: streams.top_clients,
    SupportedStreams.MEMBERS: streams.all_members,
    SupportedStreams.GROWTH_HISTORY: streams.all_growth_history
}


def stream(creds: Credentials, name: str) -> None:
    client: ApiClient = api.new_client(creds)
    _stream_executor[SupportedStreams(name)](client, None)


def stream_all(creds: Credentials) -> None:
    client: ApiClient = api.new_client(creds)
    for _, executor in _stream_executor.items():
        executor(client, None)
