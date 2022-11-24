from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_xpath_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] == "XPathNavigator":
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
