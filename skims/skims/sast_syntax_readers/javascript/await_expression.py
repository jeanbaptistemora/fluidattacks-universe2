from model.graph_model import (
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    yield from args.generic(
        args.fork_n_id(tuple(args.graph.adj[args.n_id].keys())[1])
    )
