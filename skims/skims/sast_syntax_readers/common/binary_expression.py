from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    l_id = args.graph.nodes[args.n_id]["label_field_left"]
    op_id = args.graph.nodes[args.n_id]["label_field_operator"]
    r_id = args.graph.nodes[args.n_id]["label_field_right"]

    yield graph_model.SyntaxStepBinaryExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(r_id)),
                args.generic(args.fork_n_id(l_id)),
            ],
        ),
        operator=args.graph.nodes[op_id]["label_text"],
    )
