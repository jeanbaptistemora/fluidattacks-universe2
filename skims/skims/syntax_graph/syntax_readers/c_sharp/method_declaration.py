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
from utils.graph import (
    match_ast,
    match_ast_group,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    method = args.ast_graph.nodes[args.n_id]
    name_id = method["label_field_name"]
    parameters_id = method["label_field_parameters"]
    block_id = method.get("label_field_body")

    name = node_to_str(args.ast_graph, name_id)

    if "__0__" not in match_ast(args.ast_graph, parameters_id, "(", ")"):
        parameters_id = None

    match_childs = match_ast_group(
        args.ast_graph, args.n_id, "attribute_list", "modifier"
    )
    attributes = match_childs.get("attribute_list")

    children_nid = {
        "parameters_id": parameters_id,
    }

    if attributes:
        for idx, attribute in enumerate(attributes):
            children_nid.update({f"attr_{idx}": attribute})
            print(children_nid)

    return build_method_declaration_node(args, name, block_id, children_nid)
