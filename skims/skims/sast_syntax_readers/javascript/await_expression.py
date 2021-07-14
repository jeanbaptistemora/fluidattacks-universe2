from model.graph_model import (
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, "await", "__0__")
    if len(match) > 2:
        raise MissingCaseHandling(args)

    yield from args.generic(args.fork_n_id(match["__0__"]))
