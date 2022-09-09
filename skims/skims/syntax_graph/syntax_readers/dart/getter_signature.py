# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.getter_signature import (
    build_getter_signature_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node_attrs = args.ast_graph.nodes[args.n_id]
    name = node_to_str(args.ast_graph, node_attrs["label_field_name"])
    c_ids = adj_ast(args.ast_graph, args.n_id)

    return build_getter_signature_node(args, name, iter(c_ids))
