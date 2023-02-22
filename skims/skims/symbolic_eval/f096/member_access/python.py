from symbolic_eval.common import (
    PYTHON_INPUTS,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def deserialization_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    expr = f'{n_attrs["expression"]}.{n_attrs["member"]}'

    if expr in PYTHON_INPUTS:
        args.evaluation[args.n_id] = True
        args.triggers.add("userparams")
    elif expr == "yaml.Loader":
        args.evaluation[args.n_id] = True
        args.triggers.add("dangerloader")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
