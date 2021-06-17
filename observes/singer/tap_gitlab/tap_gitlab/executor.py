import logging
from tap_gitlab import (
    streams,
)
from tap_gitlab.api.auth import (
    Credentials,
)
from tap_gitlab.api.client import (
    ApiClient,
)
from tap_gitlab.streams import (
    SupportedStreams,
)
from typing import (
    List,
)

LOG = logging.getLogger(__name__)


def stream(
    creds: Credentials, stream_name: str, projects: List[str], max_pages: int
) -> None:
    target_stream = SupportedStreams(stream_name)
    client = ApiClient(creds)
    if target_stream == SupportedStreams.MERGE_REQUESTS:
        for project in projects:
            LOG.info("Executing stream: %s at %s", target_stream, project)
            streams.all_mrs(client, project, max_pages)
    raise NotImplementedError(f"for {target_stream}")
