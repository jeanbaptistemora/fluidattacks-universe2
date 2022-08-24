from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.modifiers import (
    build_modifiers_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    annotation_id = None
    return build_modifiers_node(args, annotation_id)
