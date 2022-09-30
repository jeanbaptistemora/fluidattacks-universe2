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
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    name_id = args.ast_graph.nodes[args.n_id]["label_field_name"]
    type_annon_id = args.ast_graph.nodes[args.n_id].get("label_field_type")
    match_childs = match_ast(args.ast_graph, str(type_annon_id), ":")
    predefined_type = str(match_childs["__0__"])
    type_id = match_ast(args.ast_graph, predefined_type)["__0__"]

    return build_pair_node(args, name_id, str(type_id))
