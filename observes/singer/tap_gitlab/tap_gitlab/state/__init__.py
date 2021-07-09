from datetime import (
    datetime,
)
import pytz
from tap_gitlab.state._objs import (
    EtlState,
    JobStateMap,
    JobStatePoint,
    JobStreamState,
    MrStateMap,
    MrStreamState,
)
from tap_gitlab.state.factories import (
    fp_factory,
)


def update_mr_state(state: MrStreamState) -> MrStreamState:
    return MrStreamState(
        fp_factory.append(state.state, datetime.now(pytz.utc))
    )


def update_state(state: EtlState) -> EtlState:
    mrs = {key: update_mr_state(item) for key, item in state.mrs.items.items()}
    return EtlState(state.jobs, MrStateMap(mrs))


__all__ = [
    "MrStreamState",
    "JobStreamState",
    "JobStatePoint",
    "MrStateMap",
    "JobStateMap",
    "EtlState",
]
