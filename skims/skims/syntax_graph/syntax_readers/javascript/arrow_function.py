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
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    arrow_id = args.ast_graph.nodes[args.n_id]
    block_id = arrow_id["label_field_body"]
    params = arrow_id.get("label_field_parameter") or arrow_id.get(
        "label_field_parameters"
    )
    children_nid = {"parameters_id": params}

    return build_method_declaration_node(args, None, block_id, children_nid)
