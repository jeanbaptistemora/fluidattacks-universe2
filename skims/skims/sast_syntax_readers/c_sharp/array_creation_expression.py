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
    match = g.match_ast(
        args.graph, args.n_id, "array_type", "initializer_expression"
    )
    object_type_id = args.graph.nodes[match["array_type"]]["label_field_type"]
    yield graph_model.SyntaxStepArrayInstantiation(
        meta=graph_model.SyntaxStepMeta.default(args.n_id),
        array_type=args.graph.nodes[object_type_id]["label_text"],
    )
