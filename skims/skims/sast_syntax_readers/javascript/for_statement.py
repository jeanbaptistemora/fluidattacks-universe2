from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    initializer_id = node_attrs["label_field_initializer"]
    condition_id = node_attrs["label_field_condition"]
    increment_id = node_attrs["label_field_increment"]

    yield graph_model.SyntaxStepFor(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(initializer_id)),
            ],
        ),
        n_id_var_declaration=initializer_id,
        n_id_conditional_expression=condition_id,
        n_id_update=increment_id,
    )
