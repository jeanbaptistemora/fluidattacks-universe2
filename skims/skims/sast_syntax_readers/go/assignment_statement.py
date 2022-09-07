# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStepAssignment,
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
    operators = {
        "=",
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
        "&=",
        "|=",
        "^=",
        "<<=",
        ">>=",
        "&^=",
    }

    match = g.match_ast(args.graph, args.n_id, "__0__", "__1__", "__2__")
    operator_id = match["__1__"]
    if (
        (vars_n_id := match["__0__"])
        and operator_id
        and args.graph.nodes[operator_id]["label_type"] in operators
        and (vals_n_id := match["__2__"])
    ):
        vars_ids = g.get_ast_childs(args.graph, vars_n_id, "identifier")
        vals_ids = tuple(
            v
            for _, v in g.match_ast(args.graph, vals_n_id, ",").items()
            if v and args.graph.nodes[v]["label_type"] != ","
        )
        if len(vars_ids) == len(vals_ids):
            for var_id, val_id in zip(vars_ids, vals_ids):
                deps = [args.generic(args.fork_n_id(val_id))]
                yield SyntaxStepAssignment(
                    meta=SyntaxStepMeta.default(var_id, deps),
                    var=args.graph.nodes[var_id]["label_text"],
                )
        else:
            for var_id in vars_ids:
                deps = [
                    args.generic(args.fork_n_id(val_id)) for val_id in vals_ids
                ]
                yield SyntaxStepAssignment(
                    meta=SyntaxStepMeta.default(var_id, deps),
                    var=args.graph.nodes[var_id]["label_text"],
                )
        if not vars_ids and (
            s_id := g.get_ast_childs(
                args.graph, vars_n_id, "selector_expression"
            )
        ):
            deps = [
                args.generic(args.fork_n_id(val_id)) for val_id in vals_ids
            ]
            var_id, _, attr_id = g.adj_ast(args.graph, s_id[0])
            # Attributes with depth = 1
            if args.graph.nodes[var_id]["label_type"] == "identifier":
                yield SyntaxStepAssignment(
                    meta=SyntaxStepMeta.default(var_id, deps),
                    var=args.graph.nodes[var_id]["label_text"],
                    attribute=args.graph.nodes[attr_id]["label_text"],
                )
    else:
        raise MissingCaseHandling(args)
