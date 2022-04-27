from symbolic_eval.types import (
    SymbolicEvalArgs,
)


def evaluate(args: SymbolicEvalArgs) -> bool:
    ma_attr = args.graph.nodes[args.n_id]
    return (
        ma_attr["expression"] == "Process" and ma_attr["member"] == "Start"
    ) or ma_attr["member"] == "Execute"
