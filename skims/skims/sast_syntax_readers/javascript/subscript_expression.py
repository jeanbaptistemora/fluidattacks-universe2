# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStepMeta,
    SyntaxStepsLazy,
    SyntaxStepSubscriptExpression,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    _object_id = node_attrs["label_field_object"]
    _object = args.generic(args.fork_n_id(_object_id))
    index_id = node_attrs["label_field_index"]
    index = args.generic(args.fork_n_id(index_id))

    yield SyntaxStepSubscriptExpression(
        SyntaxStepMeta.default(args.n_id, [_object, index])
    )
