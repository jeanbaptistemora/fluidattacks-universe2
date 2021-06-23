import logging
from tap_gitlab.api.auth import (
    Credentials,
)
from tap_gitlab.emitter import (
    Emitter,
)
from tap_gitlab.streams import (
    default_job_stream,
    default_mr_streams,
    SupportedStreams,
)
from typing import (
    Union,
)

LOG = logging.getLogger(__name__)


def defautl_stream(
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
    emitter = Emitter(creds, max_pages)
    if _target_stream == SupportedStreams.JOBS:
        LOG.info("Executing stream: %s", _target_stream)
        emitter.emit_jobs(default_job_stream(project))
    elif _target_stream == SupportedStreams.MERGE_REQUESTS:
        LOG.info("Executing stream: %s", _target_stream)
        streams = default_mr_streams(project)
        for stream in streams:
            emitter.emit_mrs(stream)
    else:
        raise NotImplementedError(f"for {_target_stream}")
