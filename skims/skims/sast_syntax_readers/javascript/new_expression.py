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
    build_js_member_expression,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "new",
        "member_expression",
        "identifier",
        "arguments",
    )
    if identifier_id := match["identifier"]:
        type_name = args.graph.nodes[identifier_id]["label_text"]
    elif member_id := match["member_expression"]:
        type_name = build_js_member_expression(args.graph, member_id)
    else:
        raise MissingCaseHandling(args)

    yield graph_model.SyntaxStepObjectInstantiation(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            dependencies_from_arguments(
                args.fork_n_id(match["arguments"]),
            ),
        ),
        object_type=type_name,
    )
