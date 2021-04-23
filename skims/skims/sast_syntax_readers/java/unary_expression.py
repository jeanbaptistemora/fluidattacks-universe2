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
    op_id, exp_id = g.adj_ast(args.graph, args.n_id)

    yield graph_model.SyntaxStepUnaryExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(exp_id)),
            ],
        ),
        operator=args.graph.nodes[op_id]["label_text"],
    )
