# Local libraries
from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    # switch parenthesized_expression switch_block
    switch_c_ids = g.adj_ast(args.graph, args.n_id)
    switch_pred_id = switch_c_ids[1]
    switch_block_id = switch_c_ids[2]
    switch_label_ids = tuple(
        c_id
        for c_id in g.adj_ast(args.graph, switch_block_id)[1:-1]
        if args.graph.nodes[c_id]["label_type"] == "switch_label"
    )

    yield graph_model.SyntaxStepSwitch(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(switch_label_id))
                for switch_label_id in reversed(switch_label_ids)
            ]
            + [
                args.generic(args.fork_n_id(switch_pred_id)),
            ],
        ),
    )
