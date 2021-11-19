from syntax_cfg.dispatchers import (
    connect_to_block,
    connect_to_next,
    if_node,
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
            "MethodDeclaration",
            "Namespace",
        },
        cfg_builder=connect_to_block.build,
    ),
    Dispatcher(
        applicable_types={
            "DeclarationBlock",
            "ExecutionBlock",
            "File",
        },
        cfg_builder=step_by_step.build,
    ),
    Dispatcher(
        applicable_types={
            "If",
        },
        cfg_builder=if_node.build,
    ),
    Dispatcher(
        applicable_types={
            "MethodInvocation",
            "ThrowStatement",
            "VariableDeclaration",
        },
        cfg_builder=connect_to_next.build,
    ),
)
