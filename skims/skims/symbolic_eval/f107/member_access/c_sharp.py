from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

USER_INPUTS: set[str] = {
    "Cookies",
    "FileName",
    "Form",
    "GetString",
    "Params",
    "QueryString",
    "ReadLine",
    "ServerVariables",
}


def cs_ldap_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    if ma_attr["member"] in USER_INPUTS:
        args.triggers.add("userparameters")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
