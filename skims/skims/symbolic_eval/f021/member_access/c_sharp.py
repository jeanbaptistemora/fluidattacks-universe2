from symbolic_eval.common import (
    check_http_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

HTTP_INPUTS: set[str] = {
    "Params",
    "QueryString",
    "Form",
    "Cookies",
    "ServerVariables",
    "ReadLine",
    "GetString",
    "cookieSources",
}


def is_select_single_node(args: SymbolicEvalArgs) -> bool:
    ma_attr = args.graph.nodes[args.n_id]
    expr_id = ma_attr["expression_id"]

    if args.evaluation[expr_id] and ma_attr["member"] == "SelectSingleNode":
        return True
    return False


def cs_xpath_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if check_http_inputs(args) or is_select_single_node(args):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def cs_insec_addheader_write(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    ma_attr = args.graph.nodes[args.n_id]
    if ma_attr["member"] in HTTP_INPUTS:
        expr_nid = ma_attr["expression_id"]
        expr_eval = args.generic(args.fork(n_id=expr_nid, triggers=set()))
        if expr_eval and expr_eval.danger:
            args.triggers.add("userconnection")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
