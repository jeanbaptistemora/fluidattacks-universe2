from model.graph_model import (
    Graph,
    NId,
)
from syntax_cfg.dispatchers import (
    DISPATCHERS,
)
from syntax_cfg.types import (
    MissingCfgBuilder,
    SyntaxCfgArgs,
)
from utils import (
    logs,
)


def generic(args: SyntaxCfgArgs) -> NId:
    node_type = args.graph.nodes[args.n_id]["label_type"]

    for dispatcher in DISPATCHERS:
        if node_type in dispatcher.applicable_types:
            return dispatcher.cfg_builder(args)

    raise MissingCfgBuilder(f"Missing cfg builder for {node_type}")


def build_syntax_cfg(graph: Graph) -> bool:
    try:
        generic(args=SyntaxCfgArgs(generic, graph, n_id="1", nxt_id=None))
        return True
    except MissingCfgBuilder as error:
        logs.log_blocking("warning", error)
        return False
