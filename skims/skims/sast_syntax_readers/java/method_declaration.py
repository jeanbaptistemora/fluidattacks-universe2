# Local libraries
from typing import Set
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
    for ps_id in g.get_ast_childs(args.graph, args.n_id, "formal_parameters"):
        for p_id in g.get_ast_childs(args.graph, ps_id, "formal_parameter"):
            yield from method_declaration_formal_parameter(
                args.fork_n_id(p_id)
            )


def method_declaration_formal_parameter(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "type_identifier",
        "identifier",
        "modifiers",
        "generic_type",
    )
    if (
        len(match) == 4
        and (
            (var_type_id := match["type_identifier"])
            or (var_type_id := match["generic_type"])
        )
        and (var_id := match["identifier"])
    ):
        modifiers_name: Set[str] = set()
        if modifiers := match["modifiers"]:
            for decorator in g.get_ast_childs(
                args.graph,
                modifiers,
                "marker_annotation",
            ):
                decorator_name_id = args.graph.nodes[decorator][
                    "label_field_name"
                ]
                modifiers_name.add(
                    args.graph.nodes[decorator_name_id]["label_text"]
                )

        var_type_str: str = args.graph.nodes[var_type_id]["label_text"]
        if match["generic_type"]:
            var_type_str = var_type_str.split("<")[0]

        yield graph_model.SyntaxStepDeclaration(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            var=args.graph.nodes[var_id]["label_text"],
            var_type=var_type_str,
            modifiers=modifiers_name,
        )
    else:
        raise MissingCaseHandling(args)
