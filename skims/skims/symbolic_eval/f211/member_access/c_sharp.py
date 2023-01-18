from symbolic_eval.common import (
    HTTP_INPUTS,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_METHODS = {
    "QueryString",
    "ReadLine",
    "GetString",
    "Cookies",
    "FileName",
}


def cs_regex_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    member_access = f'{ma_attr["expression"]}.{ma_attr["member"]}'
    args.evaluation[args.n_id] = member_access in HTTP_INPUTS
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def cs_vuln_regex(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    args.evaluation[args.n_id] = False

    if ma_attr["member"] in DANGER_METHODS:
        args.triggers.add("userparams")

    if ma_attr["expression"] == "TimeSpan":
        args.triggers.add("hastimespan")

    if ma_attr["member"] == "Escape":
        args.triggers.add("safepattern")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
