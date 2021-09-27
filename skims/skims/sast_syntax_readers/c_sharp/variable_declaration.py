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
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match_declaration = g.match_ast_group(
        args.graph,
        args.n_id,
        "variable_declarator",
        "__0__",
    )
    var_type_id = match_declaration["__0__"]
    var_declarators = match_declaration["variable_declarator"]
    if not var_declarators:
        raise MissingCaseHandling(args)

    for var_declarator in var_declarators or set():
        match_declarator = g.match_ast(
            args.graph,
            var_declarator,
            "identifier",
            "equals_value_clause",
        )
        type_identifier = match_declarator["identifier"]
        deps_src = []
        if equals_value := match_declarator["equals_value_clause"]:
            match_equals = g.match_ast(
                args.graph,
                equals_value,
                "=",
                "__0__",
            )
            if match_equals["="] and (deps_id := match_equals["__0__"]):
                deps_src = [args.generic(args.fork_n_id(deps_id))]

        if args.graph.nodes[var_type_id]["label_type"] == "qualified_name":
            var_type = node_to_str(args.graph, var_type_id)
        elif label_text := args.graph.nodes[var_type_id].get("label_text"):
            var_type = label_text
        else:
            var_type = args.graph.nodes[var_type_id]["label_type"]

        yield graph_model.SyntaxStepDeclaration(
            meta=graph_model.SyntaxStepMeta.default(args.n_id, deps_src),
            var=args.graph.nodes[type_identifier]["label_text"],
            var_type=var_type,
        )
