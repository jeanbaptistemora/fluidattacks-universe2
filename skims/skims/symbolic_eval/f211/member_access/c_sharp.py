from symbolic_eval.common import (
    HTTP_INPUTS,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_regex_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    member_access = f'{ma_attr["expression"]}.{ma_attr["member"]}'
    args.evaluation[args.n_id] = member_access in HTTP_INPUTS
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def cs_vuln_regex(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    args.evaluation[args.n_id] = False

    if ma_attr["expression"] == "TimeSpan" or ma_attr["member"] == "Escape":
        args.triggers.add("SafeRegex")
    else:
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
