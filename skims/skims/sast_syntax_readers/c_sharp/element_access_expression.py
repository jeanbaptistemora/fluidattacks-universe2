from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph, args.n_id, "__0__", "bracketed_argument_list"
    )

    if (object_id := match["__0__"]) and (
        bracket := match["bracketed_argument_list"]
    ):
        match_bracket = g.match_ast(
            args.graph, bracket, "__0__", "__1__", "__2__"
        )
        yield graph_model.SyntaxStepArrayAccess(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(object_id)),
                    args.generic(args.fork_n_id(match_bracket["__1__"])),
                ],
            ),
        )
    else:
        raise MissingCaseHandling(args)
