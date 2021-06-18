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
    Union,
)

LOG = logging.getLogger(__name__)


def stream(
    creds: Credentials,
    target_stream: Union[str, SupportedStreams],
    project: str,
    max_pages: int,
) -> None:
    _target_stream = (
        SupportedStreams(target_stream)
        if isinstance(target_stream, str)
        else target_stream
    )
    client = ApiClient(creds)
    if _target_stream == SupportedStreams.MERGE_REQUESTS:
        LOG.info("Executing stream: %s", _target_stream)
        streams.all_mrs(client, project, max_pages)
    raise NotImplementedError(f"for {_target_stream}")


def stream_all(creds: Credentials, project: str, max_pages: int) -> None:
    for target in SupportedStreams:
        stream(creds, target, project, max_pages)
