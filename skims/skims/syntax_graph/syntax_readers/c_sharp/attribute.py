from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.attribute import (
    build_attribute_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    children = match_ast(args.ast_graph, args.n_id, "identifier")
    if identifier := children.get("identifier"):
        attr_name = args.ast_graph.nodes[identifier].get("label_text")
        return build_attribute_node(args, attr_name)

    raise MissingCaseHandling(f"Bad attribute handling in {args.n_id}")
