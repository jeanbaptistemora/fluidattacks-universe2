from model.graph_model import (
    SyntaxStepMeta,
    SyntaxStepNamedArgument,
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
    first_child, *other_childs = g.adj_ast(args.graph, args.n_id)

    if other_childs:
        # argument : value -> name_colon __0__
        #                     name_colon -> identifier :
        match = g.match_ast(args.graph, args.n_id, "name_colon")

        if name_colon := match["name_colon"]:
            identifier_id = g.match_ast_d(args.graph, name_colon, "identifier")

            yield SyntaxStepNamedArgument(
                meta=SyntaxStepMeta.default(
                    args.n_id,
                    dependencies=[
                        args.generic(args.fork_n_id(match["__0__"])),
                    ],
                ),
                var=args.graph.nodes[identifier_id]["label_text"],
            )
        else:
            raise MissingCaseHandling(args)
    else:
        # argument is a simple expression
        yield from args.generic(args.fork_n_id(first_child))
