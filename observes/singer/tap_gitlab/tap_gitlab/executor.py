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
from tap_gitlab.api.client import (
    ApiClient,
)
from tap_gitlab.emitter import (
    Emitter,
)
from tap_gitlab.intervals.interval.factory import (
    IntervalFactory,
)
from tap_gitlab.state import (
    EtlState,
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


def mr_stream(emitter: Emitter, state: EtlState) -> EtlState:
    LOG.info("Executing stream: %s", SupportedStreams.MERGE_REQUESTS)
    for stream in state.mrs.items.keys():
        result = emitter.emit_mrs(stream, state.mrs.items[stream])
        state.mrs.items[stream] = result  # state mutation
        LOG.debug("new status: %s", result)
    return state


def job_stream(emitter: Emitter, state: EtlState) -> EtlState:
    if state.jobs:
        LOG.info("Executing stream: %s", SupportedStreams.JOBS)
        for stream in state.jobs.items.keys():
            result = emitter.emit_jobs(stream, state.jobs.items[stream])
            state.jobs.items[stream] = result  # state mutation
            LOG.debug("new status: %s", result)
    else:
        LOG.warning(
            "Stream %s skipped. Stream state missing", SupportedStreams.JOBS
        )
    return state


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
    emitter = Emitter(ApiClient(creds), max_pages)
    if _target_stream in (SupportedStreams.JOBS, SupportedStreams.ALL):
        _state = job_stream(emitter, _state)
    if _target_stream in (
        SupportedStreams.MERGE_REQUESTS,
        SupportedStreams.ALL,
    ):
        _state = mr_stream(emitter, _state)

    json_state = state_encoder.encode_etl_state(_state)
    emit(SingerState(json_state))
