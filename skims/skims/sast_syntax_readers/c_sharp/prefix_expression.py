from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    c_ids = g.adj_ast(args.graph, args.n_id)

    if len(c_ids) != 2:
        raise MissingCaseHandling(args)

    prefix_id, expression_id = c_ids

    yield graph_model.SyntaxStepPrefixExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(expression_id)),
            ],
        ),
        prefix=args.graph.nodes[prefix_id]["label_text"],
    )
