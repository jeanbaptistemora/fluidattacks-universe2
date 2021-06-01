from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
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
    match = g.match_ast(args.graph, args.n_id, "__0__", "__1__")
    if (
        len(match) == 2
        and (var_type := match["__0__"])
        and (var_identifier := match["__1__"])
    ):
        type_node = args.graph.nodes[var_type]
        if var_type_text := args.graph.nodes[var_type].get("label_text"):
            var_type_str = var_type_text
        elif "label_text" not in type_node and (
            array_type := type_node.get("label_field_type")
        ):
            var_type_str = args.graph.nodes[array_type]["label_text"]
        else:
            raise MissingCaseHandling(args)

        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(args.n_id),
            var=args.graph.nodes[var_identifier]["label_text"],
            var_type=var_type_str,
        )
    else:
        raise MissingCaseHandling(args)
