# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStep,
    SyntaxStepLoop,
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
    dependencies = []
    if init_id := node_attrs.get("label_field_init"):
        dependencies.append(args.generic(args.fork_n_id(init_id)))
    if condition_id := node_attrs.get("label_field_condition"):
        dependencies.append(args.generic(args.fork_n_id(condition_id)))

    yield SyntaxStepLoop(
        meta=SyntaxStepMeta.default(args.n_id, dependencies),
    )
