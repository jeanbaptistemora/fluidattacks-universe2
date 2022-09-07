# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    n_id_false = node_attrs.get("label_field_alternative")
    if not n_id_false:
        # Read the else branch by following the CFG, if such branch exists
        c_ids = g.adj_cfg(args.graph, args.n_id)
        if len(c_ids) >= 2:
            n_id_false = c_ids[1]

    yield graph_model.SyntaxStepIf(
        meta=graph_model.SyntaxStepMeta.default(
            n_id=args.n_id,
            dependencies=dependencies_from_arguments(
                args.fork_n_id(node_attrs["label_field_condition"]),
            ),
        ),
        n_id_false=n_id_false,
        n_id_true=node_attrs["label_field_consequence"],
    )
