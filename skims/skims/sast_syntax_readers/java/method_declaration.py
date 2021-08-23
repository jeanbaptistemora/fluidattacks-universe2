from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Set,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    parameters_id = args.graph.nodes[args.n_id]["label_field_parameters"]
    for p_id in g.get_ast_childs(
        args.graph, parameters_id, "formal_parameter"
    ):
        yield from method_declaration_formal_parameter(args.fork_n_id(p_id))


def method_declaration_formal_parameter(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    var_type_id = node_attrs["label_field_type"]
    var_id = node_attrs["label_field_name"]
    match = g.match_ast(args.graph, args.n_id, "modifiers")

    modifiers_name: Set[str] = set()
    if modifiers := match["modifiers"]:
        match_modifiers = g.match_ast_group(
            args.graph, modifiers, "annotation", "marker_annotation"
        )

        for decorator in (
            match_modifiers["marker_annotation"]
            + match_modifiers["annotation"]
        ):
            decorator_name_id = args.graph.nodes[decorator]["label_field_name"]
            modifiers_name.add(
                args.graph.nodes[decorator_name_id]["label_text"]
            )

    var_type_str: str = args.graph.nodes[var_type_id]["label_text"]
    if args.graph.nodes[var_type_id]["label_type"] == "generic_type":
        var_type_str = var_type_str.split("<")[0]

    yield graph_model.SyntaxStepDeclaration(
        meta=graph_model.SyntaxStepMeta.default(args.n_id),
        var=args.graph.nodes[var_id]["label_text"],
        var_type=var_type_str,
        modifiers=modifiers_name,
    )
