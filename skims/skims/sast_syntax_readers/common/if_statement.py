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
    condition_id = args.graph.nodes[args.n_id]["label_field_condition"]
    n_id_true = args.graph.nodes[args.n_id]["label_field_consequence"]
    n_id_false = args.graph.nodes[args.n_id].get("label_field_alternative")

    if not n_id_false:
        # Read the else branch by following the CFG, if such branch exists
        c_ids = g.adj_cfg(args.graph, args.n_id)
        if len(c_ids) == 2:  # then clause and node after that
            _, n_id_false = c_ids

    yield graph_model.SyntaxStepIf(
        meta=graph_model.SyntaxStepMeta.default(
            n_id=args.n_id,
            dependencies=[
                args.generic(args.fork_n_id(condition_id)),
            ],
        ),
        n_id_false=n_id_false,
        n_id_true=n_id_true,
    )
