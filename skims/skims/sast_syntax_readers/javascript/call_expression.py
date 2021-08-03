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
from utils.graph.transformation import (
    build_js_member_expression_key,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    arguments_id = node_attrs["label_field_arguments"]
    function_id = node_attrs["label_field_function"]
    function_attrs = args.graph.nodes[function_id]

    if function_attrs["label_type"] == "member_expression":
        method_name = build_js_member_expression_key(args.graph, function_id)
    elif function_attrs["label_type"] == "identifier":
        method_name = args.graph.nodes[function_id]["label_text"]
    else:
        raise MissingCaseHandling(args)

    yield graph_model.SyntaxStepMethodInvocation(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            dependencies_from_arguments(
                args.fork_n_id(arguments_id),
            ),
        ),
        method=method_name,
        current_instance=graph_model.CurrentInstance(fields={}),
    )
