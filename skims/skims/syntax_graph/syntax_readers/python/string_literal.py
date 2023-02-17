from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.string_literal import (
    build_string_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    text = node_to_str(graph, args.n_id)
    if interp_id := match_ast_d(graph, args.n_id, "interpolation"):
        childs = adj_ast(graph, interp_id)
        filtered_ids = (
            _id
            for _id in childs
            if args.ast_graph.nodes[_id]["label_type"] not in {"{", "}"}
        )

        return build_string_literal_node(args, text, iter(filtered_ids), None)

    return build_string_literal_node(args, text)
