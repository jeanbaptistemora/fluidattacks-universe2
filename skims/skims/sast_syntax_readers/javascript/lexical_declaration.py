from model.graph_model import (
    SyntaxStep,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    match = g.match_ast(args.graph, args.n_id, "variable_declarator")
    yield from args.generic(args.fork_n_id(str(match["variable_declarator"])))
