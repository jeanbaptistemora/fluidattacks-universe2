from model.graph_model import (
    Graph,
)
from syntax_cfg.dispatchers import (
    DISPATCHERS,
)
from syntax_cfg.types import (
    MissingCfgBuilder,
    Stack,
    SyntaxCfgArgs,
)


def generic(args: SyntaxCfgArgs, stack: Stack) -> None:
    node_type = args.graph.nodes[args.n_id]["label_type"]

    for dispatcher in DISPATCHERS:
        if node_type in dispatcher.applicable_types:
            dispatcher.cfg_builder(args, stack)
            return

    raise MissingCfgBuilder(f"Missing cfg builder for {node_type}")


def build_syntax_cfg(graph: Graph) -> bool:
    try:
        generic(args=SyntaxCfgArgs(generic, graph, n_id="1"), stack=[])
        return True
    except MissingCfgBuilder as error:
        print(error)
        return False
