from symbolic_eval.common import (
    check_python_inputs,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def xml_parser(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if check_python_inputs(args):
        args.evaluation[args.n_id] = True
        args.triggers.add("userparams")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
