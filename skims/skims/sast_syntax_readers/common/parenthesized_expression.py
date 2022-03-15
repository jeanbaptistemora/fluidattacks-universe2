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
        "type_identifier",
        "(",
        ")",
        "__0__",
    )
    yield graph_model.SyntaxStepParenthesizedExpression(
        meta=graph_model.SyntaxStepMeta.default(
            n_id=args.n_id,
            dependencies=[
                args.generic(args.fork_n_id(str(match["__0__"]))),
            ],
        ),
    )
