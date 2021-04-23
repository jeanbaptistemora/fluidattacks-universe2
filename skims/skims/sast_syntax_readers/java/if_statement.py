# Local libraries
from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    # if ( __0__ ) __1__ else __2__
    match = g.match_ast(
        args.graph,
        args.n_id,
        "if",
        "__0__",
        "__1__",
        "else",
        "__2__",
    )

    n_id_false = match["__2__"]
    if not n_id_false:
        # Read the else branch by following the CFG, if such branch exists
        c_ids = g.adj_cfg(args.graph, args.n_id)
        if len(c_ids) >= 2:
            n_id_false = c_ids[1]

    yield graph_model.SyntaxStepIf(
        meta=graph_model.SyntaxStepMeta.default(
            n_id=args.n_id,
            dependencies=dependencies_from_arguments(
                args.fork_n_id(match["__0__"]),
            ),
        ),
        n_id_false=n_id_false,
        n_id_true=match["__1__"],
    )
