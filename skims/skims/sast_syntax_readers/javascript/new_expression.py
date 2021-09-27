from model import (
    graph_model,
)
from model.graph_model import (
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    constructor_id = node_attrs["label_field_constructor"]
    constructor = args.graph.nodes[constructor_id]

    if constructor["label_type"] == "identifier":
        type_name = args.graph.nodes[constructor_id]["label_text"]
    elif constructor["label_type"] == "member_expression":
        type_name = node_to_str(args.graph, constructor_id)
    else:
        raise MissingCaseHandling(args)

    yield graph_model.SyntaxStepObjectInstantiation(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            dependencies_from_arguments(
                args.fork_n_id(node_attrs["label_field_arguments"]),
            )
            if "label_field_arguments" in node_attrs
            else [],
        ),
        object_type=type_name,
    )
