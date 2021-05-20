# Local libraries
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


def reader(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "for",
        "(",
        "binary_expression",
        "variable_declaration",
        "postfix_unary_expression",
        ")",
        "block",
        ";",
    )
    if (
        len(match) == 9
        and (var := match["variable_declaration"])
        and (binary := match["binary_expression"])
        and (update := match["postfix_unary_expression"])
    ):
        yield graph_model.SyntaxStepFor(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(var)),
                ],
            ),
            n_id_var_declaration=var,
            n_id_conditional_expression=binary,
            n_id_update=update,
        )
    else:
        raise MissingCaseHandling(args)
