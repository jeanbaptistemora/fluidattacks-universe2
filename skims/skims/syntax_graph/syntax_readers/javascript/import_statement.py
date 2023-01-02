from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.import_statement import (
    build_import_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Dict,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:

    node = args.ast_graph.nodes[args.n_id]
    source_id = node.get("label_field_source")
    if source_id:
        import_text = node_to_str(args.ast_graph, source_id)
    else:
        import_text = node_to_str(args.ast_graph, args.n_id)

    node_attrs: Dict[str, str] = {
        "expression": import_text,
    }

    return build_import_statement_node(args, node_attrs)
