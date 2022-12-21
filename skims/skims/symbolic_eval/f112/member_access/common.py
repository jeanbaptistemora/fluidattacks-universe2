from symbolic_eval.common import (
    JS_TS_HTTP_INPUTS,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def unsafe_sql_injection(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    if f'{n_attrs["member"]}.{n_attrs["expression"]}' in JS_TS_HTTP_INPUTS:
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
