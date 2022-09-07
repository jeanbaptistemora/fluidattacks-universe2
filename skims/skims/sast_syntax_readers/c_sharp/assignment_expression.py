# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    left_id = args.graph.nodes[args.n_id]["label_field_left"]
    right_id = args.graph.nodes[args.n_id]["label_field_right"]

    yield graph_model.SyntaxStepAssignment(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(right_id)),
            ],
        ),
        var=node_to_str(args.graph, left_id),
    )
