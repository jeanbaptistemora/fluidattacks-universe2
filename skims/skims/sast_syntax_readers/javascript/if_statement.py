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


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    node_attrs = args.graph.nodes[args.n_id]
    consequence_id = node_attrs["label_field_consequence"]
    alternative_id = node_attrs.get("label_field_alternative")

    yield graph_model.SyntaxStepIf(
        meta=graph_model.SyntaxStepMeta.default(
            n_id=args.n_id,
            dependencies=[
                args.generic(
                    args.fork_n_id(node_attrs["label_field_condition"])
                ),
            ],
        ),
        n_id_false=alternative_id,
        n_id_true=consequence_id,
    )
