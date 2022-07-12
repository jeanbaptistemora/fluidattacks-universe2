from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.lexical_declaration import (
    build_lexical_declaration_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    var_id = match_ast_d(args.ast_graph, args.n_id, "variable_declarator")
    if not var_id:
        raise MissingCaseHandling(
            f"Bad lexical declaration handling in {args.n_id}"
        )

    return build_lexical_declaration_node(args, var_id)
