from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.import_statement import (
    build_import_statement_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_id = match_ast_d(args.ast_graph, args.n_id, "scoped_identifier")
    if not c_id:
        raise MissingCaseHandling(
            f"Bad import expression handling in {args.n_id}"
        )
    import_text = node_to_str(args.ast_graph, c_id)
    return build_import_statement_node(args, import_text)
