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
from utils import (
    graph as g,
)
from utils.graph.transformation import (
    build_js_member_expression_key,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast(
        args.graph, args.n_id, "arguments", "member_expression", "identifier"
    )
    arguments_id = match["arguments"]
    if member_id := match["member_expression"]:
        method_name = build_js_member_expression_key(args.graph, member_id)
    elif identifier_id := match["identifier"]:
        method_name = args.graph.nodes[identifier_id]["label_text"]
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
