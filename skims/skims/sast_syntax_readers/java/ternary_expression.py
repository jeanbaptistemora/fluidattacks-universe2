from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "__0__",
        "?",
        "__1__",
        ":",
        "__2__",
    )

    yield graph_model.SyntaxStepTernary(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(str(match["__2__"]))),
                args.generic(args.fork_n_id(str(match["__1__"]))),
                args.generic(args.fork_n_id(str(match["__0__"]))),
            ],
        ),
    )
