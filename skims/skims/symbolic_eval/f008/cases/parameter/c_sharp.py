from symbolic_eval.types import (
    SymbolicEvalArgs,
)


def evaluate(args: SymbolicEvalArgs) -> bool:
    param_attr = args.graph.nodes[args.n_id]

    if param_attr["variable_type"] == "HttpRequest":
        param_attr["danger"] = True

    return param_attr["danger"]
