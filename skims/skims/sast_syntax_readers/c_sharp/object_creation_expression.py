# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStep,
    SyntaxStepMeta,
    SyntaxStepObjectInstantiation,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from typing import (
    Iterator,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    l_arg = "label_field_arguments"
    l_init = "label_field_initializer"
    l_type = "label_field_type"

    node_attr = args.graph.nodes[args.n_id]
    type_id = node_attr[l_type]

    dependencies = []
    if args_id := node_attr.get(l_arg):
        dependencies = dependencies_from_arguments(args.fork_n_id(args_id))
    elif init_id := node_attr.get(l_init):
        dependencies = [args.generic(args.fork_n_id(init_id))]

    yield SyntaxStepObjectInstantiation(
        meta=SyntaxStepMeta.default(
            args.n_id,
            dependencies,
        ),
        object_type=node_to_str(args.graph, type_id),
    )
