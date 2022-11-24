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
    var_type_id = args.graph.nodes[args.n_id]["label_field_type"]

    var_declarators = g.match_ast_group_d(
        args.graph,
        args.n_id,
        "variable_declarator",
    )

    if not var_declarators:
        raise MissingCaseHandling(args)

    for var_declarator in var_declarators:
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

        yield graph_model.SyntaxStepDeclaration(
            meta=graph_model.SyntaxStepMeta.default(args.n_id, deps_src),
            var=args.graph.nodes[type_identifier]["label_text"],
            var_type=node_to_str(args.graph, var_type_id),
        )
