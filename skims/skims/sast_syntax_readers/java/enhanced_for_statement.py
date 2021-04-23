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


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    # for (type foo: bar) { ... }
    match = g.match_ast(
        args.graph,
        args.n_id,
        "for",
        "(",
        "__0__",
        "__1__",
        ":",
        "__2__",
        ")",
        "block",
    )

    if (
        len(match) == 8
        and (var_type_id := match["__0__"])
        and (var_id := match["__1__"])
        and (src_id := match["__2__"])
    ):
        yield graph_model.SyntaxStepDeclaration(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(src_id)),
                ],
            ),
            var=args.graph.nodes[var_id]["label_text"],
            var_type=args.graph.nodes[var_type_id]["label_text"],
        )
    else:
        raise MissingCaseHandling(args)
