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
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "if",
        "parenthesized_expression",
        "statement_block",
        "else_clause",
    )
    statement_id = match["statement_block"]
    else_id = match["else_clause"]

    if not statement_id:
        raise MissingCaseHandling(args)

    yield graph_model.SyntaxStepIf(
        meta=graph_model.SyntaxStepMeta.default(
            n_id=args.n_id,
            dependencies=[
                args.generic(
                    args.fork_n_id(match["parenthesized_expression"])
                ),
            ],
        ),
        n_id_false=else_id,
        n_id_true=statement_id,
    )
