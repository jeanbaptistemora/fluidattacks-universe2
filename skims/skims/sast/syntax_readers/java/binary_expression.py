# Local libraries
from model import (
    graph_model,
)
from sast.syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    l_id, op_id, r_id = g.adj_ast(args.graph, args.n_id)

    yield graph_model.SyntaxStepBinaryExpression(
        meta=graph_model.SyntaxStepMeta.default(args.n_id, [
            args.generic(args.fork_n_id(r_id)),
            args.generic(args.fork_n_id(l_id)),
        ]),
        operator=args.graph.nodes[op_id]['label_text'],
    )
