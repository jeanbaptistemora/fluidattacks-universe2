from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

HTTP_INPUTS: set[str] = {
    "Cookies",
    "FileName",
    "Form",
    "GetString",
    "Params",
    "QueryString",
    "ReadLine",
    "ServerVariables",
}


def cs_insec_addheader_write(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    if ma_attr["member"] in HTTP_INPUTS:
        args.triggers.add("userparams")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
