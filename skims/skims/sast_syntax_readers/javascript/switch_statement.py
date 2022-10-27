# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model import (
    graph_model,
)
from model.graph_model import (
    SyntaxStep,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    node_attrs = args.graph.nodes[args.n_id]
    switch_cases = g.match_ast_group(
        args.graph, node_attrs["label_field_body"], "switch_case"
    )
    yield graph_model.SyntaxStepSwitch(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(switch_label_id))
                for switch_label_id in reversed(switch_cases["switch_case"])
            ]
            + [
                args.generic(args.fork_n_id(node_attrs["label_field_value"])),
            ],
        ),
    )
