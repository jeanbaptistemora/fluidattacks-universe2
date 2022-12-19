from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Set,
)

HTTP_INPUTS: Set[str] = {
    "Params",
    "QueryString",
    "Form",
    "Cookies",
    "ServerVariables",
    "ReadLine",
}


def cs_insec_addheader_write(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    ma_attr = args.graph.nodes[args.n_id]
    if ma_attr["member"] in HTTP_INPUTS:
        expr_nid = ma_attr["expression_id"]
        expr_eval = args.generic(args.fork(n_id=expr_nid, triggers=set()))
        if expr_eval and expr_eval.danger:
            args.triggers.add("userconnection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
