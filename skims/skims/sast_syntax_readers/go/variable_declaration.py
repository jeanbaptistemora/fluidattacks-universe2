from .common import (
    get_var_type,
)
from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Any,
)
from utils import (
    graph as g,
)


def get_var_type_if_present(args: SyntaxReaderArgs) -> str:
    var_type: str = ""
    next_node: str = str(int(args.n_id) + 1)
    if (
        next_node in args.graph.nodes
        and "type" in args.graph.nodes[next_node]["label_type"]
    ):
        var_type = get_var_type(args.fork_n_id(next_node))
    return var_type


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    declaration_label = args.graph.nodes[args.n_id]["label_type"]

    vars_n_id: Any = ""
    vals_n_id: Any = ""
    if declaration_label == "short_var_declaration":
        match = g.match_ast(args.graph, args.n_id, ":=", "__0__", "__1__")
        vars_n_id = match["__0__"]
        vals_n_id = match["__1__"]
    elif declaration_label in ["const_declaration", "var_declaration"]:
        spec_label = (
            "var_spec"
            if declaration_label == "var_declaration"
            else "const_spec"
        )
        vars_n_id = g.get_ast_childs(args.graph, args.n_id, spec_label)[0]
        vals_n_id = g.get_ast_childs(args.graph, vars_n_id, "expression_list")
        vals_n_id = vals_n_id[0] if vals_n_id else ""

    vars_ids = g.get_ast_childs(args.graph, vars_n_id, "identifier")
    vals_ids = (
        tuple(
            v
            for _, v in g.match_ast(args.graph, vals_n_id, ",").items()
            if v and args.graph.nodes[v]["label_type"] != ","
        )
        if vals_n_id
        else tuple()
    )
    if len(vars_ids) == len(vals_ids):
        for var_id, val_id in zip(vars_ids, vals_ids):
            deps = [args.generic(args.fork_n_id(val_id))]
            yield SyntaxStepDeclaration(
                meta=SyntaxStepMeta.default(var_id, deps),
                var=args.graph.nodes[var_id]["label_text"],
                var_type=get_var_type_if_present(args.fork_n_id(var_id)),
            )
    else:
        for var_id in vars_ids:
            deps = [
                args.generic(args.fork_n_id(val_id)) for val_id in vals_ids
            ]
            yield SyntaxStepDeclaration(
                meta=SyntaxStepMeta.default(var_id, deps),
                var=args.graph.nodes[var_id]["label_text"],
                var_type=get_var_type_if_present(args.fork_n_id(var_id)),
            )
