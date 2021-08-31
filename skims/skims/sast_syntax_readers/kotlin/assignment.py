from model.graph_model import (
    SyntaxStepAssignment,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.kotlin.common import (
    get_composite_name,
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
        "directly_assignable_expression",
        "__0__",
        "__1__",
    )
    if (var_parent := match["directly_assignable_expression"]) and (
        value := match["__1__"]
    ):
        match = g.match_ast(
            args.graph,
            var_parent,
            "simple_identifier",
            "navigation_expression",
        )
        if var_id := match["simple_identifier"]:
            yield SyntaxStepAssignment(
                meta=SyntaxStepMeta.default(
                    n_id=args.n_id,
                    dependencies=[args.generic(args.fork_n_id(value))],
                ),
                var=args.graph.nodes[var_id]["label_text"],
            )
        elif match["navigation_expression"]:
            var_name = get_composite_name(args.graph, var_parent).split(".")
            yield SyntaxStepAssignment(
                meta=SyntaxStepMeta.default(
                    n_id=args.n_id,
                    dependencies=[args.generic(args.fork_n_id(value))],
                ),
                var=".".join(var_name[:-1]),
                attribute=var_name[-1],
            )
        else:
            raise MissingCaseHandling(args)
    else:
        raise MissingCaseHandling(args)
