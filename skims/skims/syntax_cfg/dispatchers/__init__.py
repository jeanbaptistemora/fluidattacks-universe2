from syntax_cfg.dispatchers import (
    connect_to_block,
    step_by_step,
)
from syntax_cfg.types import (
    Dispatcher,
    Dispatchers,
)

DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "Class",
        },
        cfg_builder=connect_to_block.build,
    ),
    Dispatcher(
        applicable_types={
            "DeclarationBlock",
        },
        cfg_builder=step_by_step.build,
    ),
    Dispatcher(
        applicable_types={
            "ExecutionBlock",
        },
        cfg_builder=step_by_step.build,
    ),
    Dispatcher(
        applicable_types={
            "File",
        },
        cfg_builder=step_by_step.build,
    ),
    Dispatcher(
        applicable_types={
            "MethodDeclaration",
        },
        cfg_builder=connect_to_block.build,
    ),
    Dispatcher(
        applicable_types={
            "Namespace",
        },
        cfg_builder=connect_to_block.build,
    ),
)
