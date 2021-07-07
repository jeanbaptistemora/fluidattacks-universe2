from datetime import (
    datetime,
)
import pytz
from tap_gitlab.intervals.interval import (
    MIN,
)
from tap_gitlab.state import (
    EtlState,
    MrStateMap,
    MrStreamState,
)
from tap_gitlab.state.factories import (
    f_factory,
    fp_factory,
)
from tap_gitlab.streams import (
    default_mr_streams,
)


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
