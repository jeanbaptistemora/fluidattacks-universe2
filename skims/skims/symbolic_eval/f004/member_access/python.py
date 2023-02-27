from symbolic_eval.common import (
    PYTHON_INPUTS,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def python_command_execution(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    member_access = f'{n_attrs["expression"]}.{n_attrs["member"]}'
    if member_access in PYTHON_INPUTS:
        args.evaluation[args.n_id] = True
        args.triggers.add("userparams")
    elif member_access == "shlex.quote":
        args.triggers.add("safeparams")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
