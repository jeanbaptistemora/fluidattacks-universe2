# Local libraries
from model.graph_model import SyntaxStepsLazy
from sast_syntax_readers.types import SyntaxReaderArgs
from utils import graph as g


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    for ps_id in g.get_ast_childs(args.graph, args.n_id, "parameter_list"):
        for p_id in g.get_ast_childs(args.graph, ps_id, "parameter"):
            yield from args.generic(args.fork_n_id(p_id))
