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
    var_decl_id = g.match_ast_d(args.graph, args.n_id, "variable_declaration")
    yield from args.generic(args.fork_n_id(var_decl_id))
