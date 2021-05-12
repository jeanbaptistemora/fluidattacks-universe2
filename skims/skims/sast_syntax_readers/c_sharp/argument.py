# Local libraries
from model.graph_model import (
    SyntaxStepsLazy,
)

# Local imports
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import graph as g


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    chils = g.adj_ast(args.graph, args.n_id)

    if len(chils) > 1:
        raise MissingCaseHandling(args)

    yield from args.generic(args.fork_n_id(chils[0]))
