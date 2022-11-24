from model.graph_model import (
    SyntaxStep,
    SyntaxStepMeta,
    SyntaxStepSubscriptExpression,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    node_attrs = args.graph.nodes[args.n_id]
    _object_id = node_attrs["label_field_object"]
    _object = args.generic(args.fork_n_id(_object_id))
    index_id = node_attrs["label_field_index"]
    index = args.generic(args.fork_n_id(index_id))

    yield SyntaxStepSubscriptExpression(
        SyntaxStepMeta.default(args.n_id, [_object, index])
    )
