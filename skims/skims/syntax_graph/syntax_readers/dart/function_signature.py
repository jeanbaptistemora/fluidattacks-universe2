# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_declaration import (
    build_method_declaration_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
    match_ast_d,
    search_pred_until_type,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:

    body_parents = {
        "class_body",
        "extension_body",
        "lambda_expression",
        "program",
    }

    name_id = args.ast_graph.nodes[args.n_id]["label_field_name"]
    function_name = node_to_str(args.ast_graph, name_id)

    class_pred, last_c = search_pred_until_type(
        args.ast_graph,
        args.n_id,
        body_parents,
    )

    if (
        last_c
        and (
            class_childs := list(
                match_ast(args.ast_graph, class_pred).values()
            )
        )
        and (
            parameters_id := match_ast_d(
                args.ast_graph, args.n_id, "formal_parameter_list"
            )
        )
    ):
        body_id = class_childs[class_childs.index(last_c) + 1]
        return build_method_declaration_node(
            args, function_name, body_id, {"parameters_id": parameters_id}
        )

    raise MissingCaseHandling(
        f"Bad function signature handling in {args.n_id}"
    )
