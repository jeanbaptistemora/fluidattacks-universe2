from model.graph_model import (
    SyntaxStepIf,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    condition_id = args.graph.nodes[args.n_id][
        "label_field_condition_expression"
    ]
    if_stmts_body = args.graph.nodes[args.n_id]["label_field_body"]
    else_stmts_body = args.graph.nodes[args.n_id].get(
        "label_field_else_body", None
    )

    n_id_true = tuple(
        c_id
        for c_id in g.adj_ast(args.graph, if_stmts_body)
        if args.graph.nodes[c_id]["label_type"] not in {"{", "}"}
    )[0]
    n_id_false = (
        tuple(
            c_id
            for c_id in g.adj_ast(args.graph, else_stmts_body)
            if args.graph.nodes[c_id]["label_type"] not in {"{", "}"}
        )[0]
        if else_stmts_body is not None
        else None
    )
    if not n_id_false:
        # Read the else branch by following the CFG, if such branch exists
        c_ids = g.adj_cfg(args.graph, args.n_id)
        if len(c_ids) > 1:
            n_id_false = c_ids[1]
    yield SyntaxStepIf(
        meta=SyntaxStepMeta.default(
            n_id=args.n_id,
            dependencies=[args.generic(args.fork_n_id(condition_id))],
        ),
        n_id_false=n_id_false,
        n_id_true=n_id_true,
    )
