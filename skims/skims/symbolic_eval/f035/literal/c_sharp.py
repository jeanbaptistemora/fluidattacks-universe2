from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_no_password(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False

    str_value = str(args.graph.nodes[args.n_id]["value"])[1:-1]
    for arg_part in str_value.split(";"):
        if "=" in arg_part:
            var, value = arg_part.split("=", maxsplit=1)
            if var == "Password" and not value:
                args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
