from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    object_type_id = node_attrs["label_field_type"]

    dependencies = []
    if initializer := node_attrs.get("label_field_value"):
        dependencies.append(
            args.generic(args.fork_n_id(initializer)),
        )
    yield graph_model.SyntaxStepArrayInstantiation(
        meta=graph_model.SyntaxStepMeta.default(args.n_id, dependencies),
        array_type=args.graph.nodes[object_type_id]["label_text"],
    )
