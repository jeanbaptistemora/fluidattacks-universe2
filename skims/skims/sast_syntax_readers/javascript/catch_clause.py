# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStep,
    SyntaxStepCatchClause,
    SyntaxStepMeta,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    node_attrs = args.graph.nodes[args.n_id]
    # exceptions may not have an identifier
    if parameter_id := node_attrs.get("label_field_parameter"):
        yield SyntaxStepCatchClause(
            meta=SyntaxStepMeta.default(
                n_id=args.n_id,
            ),
            var=args.graph.nodes[parameter_id].get("label_text"),
        )
