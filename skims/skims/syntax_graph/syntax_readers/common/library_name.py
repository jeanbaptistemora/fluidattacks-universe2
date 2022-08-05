from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.library_name import (
    build_library_name_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    library_text = node_to_str(args.ast_graph, args.n_id)
    return build_library_name_node(args, library_text)
