# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.attribute import (
    build_attribute_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    children = match_ast(
        args.ast_graph, args.n_id, "identifier", "attribute_argument_list"
    )
    identifier = children.get("identifier")
    attr_list = children.get("attribute_argument_list")
    if not identifier:
        raise MissingCaseHandling(f"Bad attribute handling in {args.n_id}")

    attr_name = args.ast_graph.nodes[identifier].get("label_text")
    return build_attribute_node(args, attr_name, attr_list)
