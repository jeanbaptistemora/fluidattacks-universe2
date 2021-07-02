import boto3
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
from tap_gitlab.intervals.interval import (
    IntervalFactory,
    MIN,
)
from tap_gitlab.state import (
    EtlState,
    f_factory,
    fp_factory,
    MrStateMap,
    MrStreamState,
    state_decoder,
    StateGetter,
)
from tap_gitlab.streams import (
    default_job_stream,
    default_mr_streams,
    SupportedStreams,
)
from typing import (
    Optional,
    Tuple,
    Union,
)

LOG = logging.getLogger(__name__)

state_getter = StateGetter(boto3.client("s3"), state_decoder)


def default_mr_state() -> MrStreamState:
    return MrStreamState(
        fp_factory.new_fprogress(
            f_factory.from_endpoints((MIN(), datetime.now(pytz.utc))), (False,)
        )
    )


def default_etl_state(
    project: str,
) -> EtlState:
    streams = default_mr_streams(project)
    mrs_map = MrStateMap({stream: default_mr_state() for stream in streams})
    return EtlState(None, mrs_map)


def defautl_stream(
    creds: Credentials,
    target_stream: Union[str, SupportedStreams],
    project: str,
    max_pages: int,
    state_id: Optional[Tuple[str, str]] = None,
) -> None:
    _state = (
        state_getter.get(state_id[0], state_id[1])
        if state_id
        else default_etl_state(project)
    )
    _target_stream = (
        SupportedStreams(target_stream)
        if isinstance(target_stream, str)
        else target_stream
    )
    factory: IntervalFactory[datetime] = IntervalFactory.from_default(datetime)
    emitter = Emitter(creds, factory, max_pages)
    if _target_stream == SupportedStreams.JOBS:
        LOG.info("Executing stream: %s", _target_stream)
        emitter.emit_jobs(default_job_stream(project))
    elif _target_stream == SupportedStreams.MERGE_REQUESTS:
        LOG.info("Executing stream: %s", _target_stream)
        streams = default_mr_streams(project)

        for stream in streams:
            result = emitter.emit_mrs(stream, _state.mrs.items[stream])
            LOG.debug("new status: %s", result)

    else:
        raise NotImplementedError(f"for {_target_stream}")
