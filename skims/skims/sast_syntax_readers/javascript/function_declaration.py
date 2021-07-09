from model import (
    graph_model,
)
from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, "formal_parameters")
    parameters = (
        node
        for node in g.adj_ast(args.graph, match["formal_parameters"])[1:-1]
        if args.graph.nodes[node]["label_type"] not in {",", "comment"}
    )
    for parameter in parameters:
        yield from _yield_parameter(args.fork_n_id(parameter))


def _yield_parameter(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_type = args.graph.nodes[args.n_id]["label_type"]
    if node_type == "identifier":
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(args.n_id),
            var=args.graph.nodes[args.n_id]["label_text"],
            modifiers=set(),
        )
    elif node_type == "assignment_pattern":
        match = g.match_ast(args.graph, args.n_id, "identifier", "=")

        yield SyntaxStepDeclaration(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(match["__0__"])),
                ],
            ),
            var=args.graph.nodes[match["identifier"]]["label_text"],
            modifiers=set(),
        )
    else:
        raise MissingCaseHandling(args)
