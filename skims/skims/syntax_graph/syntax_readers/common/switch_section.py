# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_section import (
    build_switch_section_node,
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
    c_ids = adj_ast(args.ast_graph, args.n_id)
    skipped_labels = {
        "break_statement",
        "case_switch_label",
        "default_switch_label",
    }
    filtered_ids = (
        _id
        for _id in c_ids
        if args.ast_graph.nodes[_id]["label_type"] not in skipped_labels
    )
    return build_switch_section_node(args, cast(Iterator[str], filtered_ids))
