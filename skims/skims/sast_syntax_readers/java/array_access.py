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
    match = g.match_ast(args.graph, args.n_id, "__0__", "__2__")

    if (n_id_object := match["__0__"]) and (n_id_index := match["__2__"]):
        yield graph_model.SyntaxStepArrayAccess(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(n_id_object)),
                    args.generic(args.fork_n_id(n_id_index)),
                ],
            ),
        )
    else:
        raise MissingCaseHandling(args)
