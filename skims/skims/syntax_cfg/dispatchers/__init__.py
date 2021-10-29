from syntax_cfg.dispatchers import (
    step_by_step,
)
from syntax_cfg.types import (
    Dispatcher,
    Dispatchers,
)

DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "File",
        },
        cfg_builder=step_by_step.build,
    ),
)
