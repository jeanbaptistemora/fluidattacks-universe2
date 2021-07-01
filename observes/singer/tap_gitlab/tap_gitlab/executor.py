from datetime import (
    datetime,
)
import logging
import pytz
from tap_gitlab.api.auth import (
    Credentials,
)
from tap_gitlab.emitter import (
    Emitter,
)
from tap_gitlab.intervals.fragmented import (
    FIntervalFactory,
)
from tap_gitlab.intervals.interval import (
    IntervalFactory,
    MIN,
)
from tap_gitlab.intervals.progress import (
    FProgressFactory,
)
from tap_gitlab.state import (
    MrStreamState,
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


def default_state() -> MrStreamState:
    factory = IntervalFactory(datetime)
    f_factory = FIntervalFactory(factory)
    fp_factory = FProgressFactory(f_factory)
    return MrStreamState(
        fp_factory.new_fprogress(
            f_factory.from_endpoints((MIN(), datetime.now(pytz.utc))), (False,)
        )
    )


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
    factory: IntervalFactory[datetime] = IntervalFactory(datetime)
    emitter = Emitter(creds, factory, max_pages)
    if _target_stream == SupportedStreams.JOBS:
        LOG.info("Executing stream: %s", _target_stream)
        emitter.emit_jobs(default_job_stream(project))
    elif _target_stream == SupportedStreams.MERGE_REQUESTS:
        LOG.info("Executing stream: %s", _target_stream)
        streams = default_mr_streams(project)

        for stream in streams:
            result = emitter.emit_mrs(stream, default_state())
            LOG.debug("new status: %s", result)
            LOG.debug("new status json: %s", result.to_json())

    else:
        raise NotImplementedError(f"for {_target_stream}")
