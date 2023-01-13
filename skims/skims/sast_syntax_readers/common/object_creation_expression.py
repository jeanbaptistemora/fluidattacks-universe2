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
    match = g.match_ast(args.graph, args.n_id, "new", "__0__", "argument_list")

    if match["new"] and (object_type_id := match["__0__"]):
        yield graph_model.SyntaxStepObjectInstantiation(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
            ),
            object_type=(
                args.graph.nodes[object_type_id]
                .get("label_text", "")
                .split("<", maxsplit=1)[0]
            ),
        )
    else:
        raise MissingCaseHandling(args)
