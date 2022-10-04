# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.pair import (
    build_pair_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    get_ast_childs,
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    name_id = args.ast_graph.nodes[args.n_id]["label_field_name"]
    type_annon_id = args.ast_graph.nodes[args.n_id].get("label_field_type")
    pred_type = get_ast_childs(
        args.ast_graph, str(type_annon_id), "predefined_type"
    )
    if pred_type:
        type_id = pred_type[0]
    else:
        match_childs = match_ast(args.ast_graph, str(type_annon_id), ":")
        type_id = str(match_childs["__0__"])

    return build_pair_node(args, name_id, type_id)
