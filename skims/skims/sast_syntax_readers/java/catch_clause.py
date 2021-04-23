# Local libraries
from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "catch",
        "catch_formal_parameter",
        "block",
    )
    if (
        len(match) == 5
        and (parameter := match["catch_formal_parameter"])
        and (block := match["block"])
    ):
        match = g.match_ast(
            args.graph,
            parameter,
            "catch_type",
            "identifier",
        )
        match_type = g.match_ast(
            args.graph,
            match["catch_type"],
            "__0__",
        )
        yield graph_model.SyntaxStepCatchClause(
            meta=graph_model.SyntaxStepMeta.default(
                n_id=args.n_id,
                dependencies=dependencies_from_arguments(
                    args.fork_n_id(block),
                ),
            ),
            var=args.graph.nodes[match["identifier"]]["label_text"],
            catch_type=match_type["__0__"],
        )
    else:
        raise MissingCaseHandling(args)
