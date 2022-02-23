from symbolic_eval.types import (
    SymbolicEvalArgs,
)


def evaluate(args: SymbolicEvalArgs) -> bool:
    exp_node = args.graph.nodes[args.n_id]["expression_id"]
    expression = args.graph.nodes[exp_node]
    if (
        expression.get("member") == "Form"
        and expression.get("expression") == "Request"
    ):
        args.evaluation[args.n_id] = True
    return args.evaluation[args.n_id]
