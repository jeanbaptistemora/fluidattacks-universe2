# pylint: skip-file

import boto3
from datetime import (
    datetime,
)
import logging
from returns.maybe import (
    Maybe,
)
from singer_io.factory import (
    emit,
)
from singer_io.singer import (
    SingerState,
)
from tap_gitlab.api.auth import (
    Credentials,
)
from tap_gitlab.emitter import (
    Emitter,
)
from tap_gitlab.intervals.interval.factory import (
    IntervalFactory,
)
from tap_gitlab.state import (
    update_state,
)
from tap_gitlab.state.decoder import (
    state_decoder,
)
from tap_gitlab.state.default import (
    default_etl_state,
)
from tap_gitlab.state.encoder import (
    state_encoder,
)
from tap_gitlab.state.getter import (
    StateGetter,
)
from tap_gitlab.streams import (
    default_job_stream,
    SupportedStreams,
)
from typing import (
    Tuple,
    Union,
)

LOG = logging.getLogger(__name__)
state_getter = StateGetter(boto3.client("s3"), state_decoder)


def defautl_stream(
    creds: Credentials,
    target_stream: Union[str, SupportedStreams],
    project: str,
    max_pages: int,
    state_id: Maybe[Tuple[str, str]],
) -> None:
    _state = (
        state_id.bind(lambda sid: state_getter.get(sid[0], sid[1]))
        .map(update_state)
        .value_or(default_etl_state(project))
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
        for stream in _state.mrs.items.keys():
            result = emitter.emit_mrs(stream, _state.mrs.items[stream])
            _state.mrs.items[stream] = result
            LOG.debug("new status: %s", result)
        json_state = state_encoder.encode_etl_state(_state)
        emit(SingerState(json_state))

    else:
        raise NotImplementedError(f"for {_target_stream}")
