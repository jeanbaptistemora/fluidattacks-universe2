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
        argument_id = g.match_ast_d(args.graph, bracket, "argument")
        yield graph_model.SyntaxStepArrayAccess(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(object_id)),
                    args.generic(args.fork_n_id(argument_id)),
                ],
            ),
        )
    else:
        raise MissingCaseHandling(args)
