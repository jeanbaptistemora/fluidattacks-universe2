from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from typing import (
    Any,
    Dict,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match: Dict[str, Any] = g.match_ast_group(
        args.graph,
        args.n_id,
        "__0__",
        "variable_declarator",
        "modifiers",
    )

    if (var_type_id := match["__0__"]) and (
        var_declarations := match["variable_declarator"]
    ):
        deps_src = []
        for var_decl_id in var_declarations or set():
            match = g.match_ast(args.graph, var_decl_id, "__0__", "=", "__1__")
            if match["="] and (deps_id := match["__1__"]):
                deps_src = [args.generic(args.fork_n_id(deps_id))]
                break
        for var_decl_id in var_declarations or set():
            match = g.match_ast(args.graph, var_decl_id, "__0__")
            var_id = match["__0__"]
            yield graph_model.SyntaxStepDeclaration(
                meta=graph_model.SyntaxStepMeta.default(args.n_id, deps_src),
                var=args.graph.nodes[var_id]["label_text"],
                var_type=(
                    args.graph.nodes[var_type_id]["label_text"].split(
                        "<", maxsplit=1
                    )[0]
                ),
            )
    else:
        raise MissingCaseHandling(args)
