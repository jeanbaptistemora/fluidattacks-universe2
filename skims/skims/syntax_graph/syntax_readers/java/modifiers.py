from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.modifiers import (
    build_modifiers_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    children = match_ast(args.ast_graph, args.n_id, "annotation")
    annotation_id = children.get("annotation")

    return build_modifiers_node(args, annotation_id)
