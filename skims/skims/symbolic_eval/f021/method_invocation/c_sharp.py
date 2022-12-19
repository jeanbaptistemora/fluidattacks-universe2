from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_xpath_injection_evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    if "SecurityElement.Escape" in ma_attr["expression"]:
        args.triggers.add("Escaped")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
