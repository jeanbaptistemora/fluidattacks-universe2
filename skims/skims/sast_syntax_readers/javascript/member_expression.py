from model.graph_model import (
    SyntaxStepMemberAccessExpression,
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
    match = g.match_ast(args.graph, args.n_id, "__0__", ".", "__1__")
    if access_key := args.graph.nodes[match["__1__"]].get("label_text"):
        yield SyntaxStepMemberAccessExpression(
            meta=SyntaxStepMeta.default(
                args.n_id,
                [args.generic(args.fork_n_id(match["__0__"]))],
            ),
            member=access_key,
        )
    else:
        raise MissingCaseHandling(args)
