from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.array_type import (
    build_array_type_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    at_attrs = args.ast_graph.nodes[args.n_id]
    type_name = args.ast_graph.nodes[at_attrs["label_field_type"]][
        "label_text"
    ]
    return build_array_type_node(args, type_name)
