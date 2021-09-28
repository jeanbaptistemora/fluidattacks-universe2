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
    expression_id = args.graph.nodes[args.n_id]["label_field_expression"]
    bracket_id = args.graph.nodes[args.n_id]["label_field_subscript"]

    argument_id = g.match_ast_d(args.graph, bracket_id, "argument")
    yield graph_model.SyntaxStepArrayAccess(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(expression_id)),
                args.generic(args.fork_n_id(argument_id)),
            ],
        ),
    )
