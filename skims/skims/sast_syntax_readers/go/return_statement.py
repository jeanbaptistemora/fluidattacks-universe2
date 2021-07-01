from model.graph_model import (
    SyntaxStepMeta,
    SyntaxStepReturn,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    c_id = g.get_ast_childs(args.graph, args.n_id, "expression_list")[0]

    yield SyntaxStepReturn(
        meta=SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(r_id))
                for r_id in g.adj_ast(args.graph, c_id)
                if args.graph.nodes[r_id]["label_type"] != ","
            ],
        )
    )
