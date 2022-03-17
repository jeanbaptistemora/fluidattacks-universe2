from model.graph_model import (
    CurrentInstance,
    SyntaxStepMeta,
    SyntaxStepMethodInvocation,
    SyntaxStepsLazy,
)
from sast_syntax_readers.kotlin.common import (
    get_composite_name,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "simple_identifier",
        "navigation_expression",
        "call_suffix",
    )

    method_name: str = ""
    if match["navigation_expression"]:
        method_name = get_composite_name(args.graph, args.n_id)
    if method_name_id := match["simple_identifier"]:
        method_name = args.graph.nodes[method_name_id]["label_text"]

    dependencies = []
    if arguments := g.get_ast_childs(
        args.graph, str(match["call_suffix"]), "value_argument", depth=2
    ):
        dependencies = [
            args.generic(args.fork_n_id(argument))
            for argument_parent in arguments
            for argument in g.adj_ast(args.graph, argument_parent)
        ]

    if method_name:
        yield SyntaxStepMethodInvocation(
            meta=SyntaxStepMeta.default(
                n_id=args.n_id,
                dependencies=dependencies,
            ),
            method=method_name,
            current_instance=CurrentInstance(fields={}),
        )
    else:
        raise MissingCaseHandling(args)
