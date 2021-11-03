from symbolic_eval.types import (
    SymbolicEvalArgs,
)


def evaluate(args: SymbolicEvalArgs) -> bool:
    expression_id = args.graph.nodes[args.n_id]["expression_id"]
    arguments_id = args.graph.nodes[args.n_id]["arguments_id"]

    d_expression = args.generic(args.fork_n_id(expression_id))
    d_arguments = args.generic(args.fork_n_id(arguments_id))

    args.graph.nodes[args.n_id]["danger"] = d_expression or d_arguments

    # finding specific check

    return args.graph.nodes[args.n_id]["danger"]
