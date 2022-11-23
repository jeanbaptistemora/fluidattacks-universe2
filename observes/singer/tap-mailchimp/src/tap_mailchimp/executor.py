import logging
from tap_mailchimp import (
    api,
    streams,
)
from tap_mailchimp.api import (
    ApiClient,
)
from tap_mailchimp.auth import (
    Credentials,
)
from tap_mailchimp.streams import (
    SupportedStreams,
)
from typing import (
    Callable,
    IO,
    Mapping,
    Optional,
)

LOG = logging.getLogger(__name__)

_stream_executor: Mapping[
    SupportedStreams, Callable[[ApiClient, Optional[IO[str]]], None]
] = {
    SupportedStreams.AUDIENCES: streams.all_audiences,
    SupportedStreams.ABUSE_REPORTS: streams.all_abuse_reports,
    SupportedStreams.GROWTH_HISTORY: streams.all_growth_history,
    SupportedStreams.INTEREST_CATEGORY: streams.all_interest_category,
    SupportedStreams.LOCATIONS: streams.all_locations,
    SupportedStreams.MEMBERS: streams.all_members,
    SupportedStreams.RECENT_ACTIVITY: streams.recent_activity,
    SupportedStreams.TOP_CLIENTS: streams.top_clients,
    SupportedStreams.CAMPAIGNS: streams.all_campaigns,
    SupportedStreams.CHECKLIST: streams.all_checklists,
    SupportedStreams.FEEDBACK: streams.all_feedback,
}


def stream(creds: Credentials, name: str) -> None:
    target_stream = SupportedStreams(name)
    LOG.info("Executing stream: %s", target_stream)
    client: ApiClient = api.new_client(creds)
    _stream_executor[target_stream](client, None)


def stream_all(creds: Credentials) -> None:
    client: ApiClient = api.new_client(creds)
    for target_stream, executor in _stream_executor.items():
        LOG.info("Executing stream: %s", target_stream)
        executor(client, None)
