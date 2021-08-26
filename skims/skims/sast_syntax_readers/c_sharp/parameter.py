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


def _get_var_type(args: SyntaxReaderArgs, type_id: str) -> str:
    type_node = args.graph.nodes[type_id]

    if var_type_text := type_node.get("label_text"):
        return var_type_text

    if array_type := type_node.get("label_field_type"):
        return args.graph.nodes[array_type]["label_text"]

    raise MissingCaseHandling(args)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, "__0__", "__1__")
    type_id = match["__0__"]
    identifier_id = match["__1__"]

    if len(match) != 2 or identifier_id is None:
        raise MissingCaseHandling(args)

    yield SyntaxStepDeclaration(
        meta=SyntaxStepMeta.default(args.n_id),
        var=args.graph.nodes[identifier_id]["label_text"],
        var_type=None if type_id is None else _get_var_type(args, type_id),
    )
