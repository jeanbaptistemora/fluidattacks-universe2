from symbolic_eval.common import (
    check_http_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from typing import (
    Set,
)

HTTP_INPUTS: Set[str] = {
    "Cookies",
    "FileName",
    "Form",
    "GetString",
    "Params",
    "QueryString",
    "ReadLine",
    "ServerVariables",
}


def cs_open_redirect(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = check_http_inputs(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def cs_unsafe_path_traversal(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    if ma_attr["member"] in HTTP_INPUTS:
        args.triggers.add("userparameters")
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
