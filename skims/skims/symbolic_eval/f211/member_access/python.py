from symbolic_eval.common import (
    PYTHON_INPUTS,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def python_regex_dos(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    expr = f'{n_attrs["expression"]}.{n_attrs["member"]}'
    if expr in PYTHON_INPUTS:
        args.evaluation[args.n_id] = True
        args.triggers.add("userparams")
    elif expr == "re.escape":
        args.triggers.add("sanitizedparams")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
