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
    match = g.match_ast(args.graph, args.n_id, "identifier")
    if len(match) == 1:
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(args.n_id),
            var=args.graph.nodes[match["identifier"]]["label_text"],
        )
    elif len(match) == 3:
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(match["__1__"])),
                ],
            ),
            var=args.graph.nodes[match["identifier"]]["label_text"],
        )
    else:
        raise MissingCaseHandling(args)
