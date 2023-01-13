from fa_purity import (
    Cmd,
)
from fa_purity.pure_iter.transform import (
    consume,
)
from fa_singer_io.singer.emitter import (
    emit,
)
import sys
from tap_mandrill.api import (
    ApiClient,
)
from tap_mandrill.singer.activity import (
    ActivitySingerEncoder,
)
from tap_mandrill.singer.core import (
    DataStreams,
)
from tap_mandrill.streams.activity import (
    all_activity,
)


def emit_stream(client: ApiClient, stream: DataStreams) -> Cmd[None]:
    if stream is DataStreams.activity:
        emit_schema = emit(sys.stdout, ActivitySingerEncoder.schema())
        emit_data = all_activity(client.export_api()).bind(
            lambda p: p.map(ActivitySingerEncoder.to_singer)
            .map(lambda s: emit(sys.stdout, s))
            .transform(consume)
        )
        return emit_schema + emit_data
