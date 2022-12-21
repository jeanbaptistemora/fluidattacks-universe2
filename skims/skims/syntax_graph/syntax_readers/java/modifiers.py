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
    graph = args.ast_graph
    annotation_ids = match_ast_group_d(
        graph, args.n_id, "annotation"
    ) + match_ast_group_d(graph, args.n_id, "marker_annotation")
    return build_modifiers_node(args, annotation_ids)
