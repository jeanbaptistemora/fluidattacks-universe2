# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.parameter import (
    build_parameter_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    cast,
    Iterator,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = [
        c_id
        for c_id in adj_ast(args.ast_graph, args.n_id)
        if args.ast_graph.nodes[c_id].get("label_type") != "type_annotation"
    ]
    return build_parameter_node(args, None, None, cast(Iterator[str], c_ids))
