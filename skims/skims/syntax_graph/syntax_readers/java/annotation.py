from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.annotation import (
    build_annotation_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    children = match_ast(
        graph, args.n_id, "identifier", "annotation_argument_list"
    )
    if identifier := children.get("identifier"):
        attr_name = graph.nodes[identifier].get("label_text")
        al_id = children.get("annotation_argument_list")
        return build_annotation_node(args, attr_name, al_id)

    raise MissingCaseHandling(f"Bad annotation handling in {args.n_id}")
