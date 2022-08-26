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
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    annotation_ids = match_ast_group_d(args.ast_graph, args.n_id, "annotation")

    return build_modifiers_node(args, annotation_ids)
