from model.graph_model import (
    Graph,
    NId,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from typing import (
    Optional,
    Tuple,
)
from utils import (
    graph as g,
)


def get_composite_name(graph: Graph, n_id: NId) -> str:
    # Function to build the name of a function/argument that has multiple
    # levels, e.g. ConnectionSpec.Builder.tlsVersions
    # For it to work, n_id must have children nodes of the type
    # `navigation_expression`.
    # n_id itself should not be a `navigation_expression` node, use its parent
    def _join_name(graph: Graph, name: str, n_id: NId) -> str:
        return g.concatenate_label_text(graph, g.adj_ast(graph, n_id)) + name

    composite_name: str = ""
    match = g.match_ast(
        graph,
        n_id,
        "navigation_expression",
        "simple_identifier",
    )
    while nav_expr := match["navigation_expression"]:
        match = g.match_ast(
            graph,
            nav_expr,
            "call_expression",
            "navigation_expression",
            "navigation_suffix",
            "simple_identifier",
            "super_expression",
            "this_expression",
        )
        composite_name = _join_name(
            graph, composite_name, match["navigation_suffix"]
        )
        if this_expr := match["this_expression"]:
            composite_name = _join_name(graph, composite_name, this_expr)
        if super_expr := match["super_expression"]:
            composite_name = _join_name(graph, composite_name, super_expr)
        if call_expr := match["call_expression"]:
            match = g.match_ast(
                graph,
                call_expr,
                "navigation_expression",
                "simple_identifier",
            )
    if name_id := match["simple_identifier"]:
        composite_name = graph.nodes[name_id]["label_text"] + composite_name
    return composite_name


def get_var_id_type(
    args: SyntaxReaderArgs, n_id: NId
) -> Tuple[Optional[str], str]:
    match = g.match_ast(
        args.graph,
        n_id,
        "nullable_type",
        "simple_identifier",
        "user_type",
    )
    var_id: Optional[str] = match["simple_identifier"]
    if var_id is None:
        raise MissingCaseHandling(args)

    var_type_parent: Optional[str] = match["user_type"]
    var_type: str = ""
    if (
        var_type_parent is None
        and (null_type := match["nullable_type"])
        and (c_ids := g.get_ast_childs(args.graph, null_type, "user_type"))
    ):
        var_type_parent = c_ids[0]
    if (
        var_id
        and var_type_parent
        and (
            var_type_id := g.get_ast_childs(
                args.graph, var_type_parent, "type_identifier"
            )
        )
    ):
        var_type = args.graph.nodes[var_type_id[0]]["label_text"]
        if match["nullable_type"]:
            var_type += "?"
    return args.graph.nodes[var_id]["label_text"], var_type
