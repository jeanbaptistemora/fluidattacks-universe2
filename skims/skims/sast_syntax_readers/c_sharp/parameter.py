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

    if "label_text" in type_node:
        return type_node["label_text"]

    if type_node["label_type"] == "array_type":
        return args.graph.nodes[type_node["label_field_type"]]["label_text"]

    raise MissingCaseHandling(args)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    childs = g.adj_ast(args.graph, args.n_id)
    if len(childs) > 2:
        raise MissingCaseHandling(args)

    node = args.graph.nodes[args.n_id]

    type_id = node.get("label_field_type")
    identifier_id = node.get("label_field_name")

    yield SyntaxStepDeclaration(
        meta=SyntaxStepMeta.default(args.n_id),
        var=args.graph.nodes[identifier_id]["label_text"],
        var_type=None if type_id is None else _get_var_type(args, type_id),
    )
