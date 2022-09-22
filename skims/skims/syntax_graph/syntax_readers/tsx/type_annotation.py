# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.type_annotation import (
    build_type_annotation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:

    childs_id = adj_ast(
        args.ast_graph,
        args.n_id,
    )

    primary_types = {
        "array_type",
        "conditional_type",
        "existential_type",
        "flow_maybe_type",
        "generic_type",
        "index_type_query",
        "intersection_type",
        "literal_type",
        "lookup_type",
        "nested_type_identifier",
        "object_type",
        "parenthesized_type",
        "predefined_type",
        "template_literal_type",
        "this_type",
        "tuple_type",
        "type_identifier",
        "type_query",
        "union_type",
    }

    valid_childs = [
        child
        for child in childs_id
        if args.ast_graph.nodes[child]["label_type"] in primary_types
    ]

    return build_type_annotation_node(args, valid_childs)
