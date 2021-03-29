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
    return_id = g.adj_ast(args.graph, args.n_id)[1]

    yield graph_model.SyntaxStepReturn(
        meta=graph_model.SyntaxStepMeta.default(args.n_id, [
            args.generic(args.fork_n_id(return_id)),
        ]),
    )
