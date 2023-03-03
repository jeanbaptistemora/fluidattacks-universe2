from symbolic_eval.common import (
    INSECURE_MODES,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

INSECURE_ALGOS = {
    "TripleDES",
    "Blowfish",
    "ARC4",
}


def python_unsafe_ciphers(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    member = n_attrs["member"]
    expr = n_attrs["expression"]

    if member in INSECURE_ALGOS and expr == "algorithms":
        args.evaluation[args.n_id] = True
        # Any mode is dangerous with these algorithms
        args.triggers.add("unsafemode")
    if member == "AES" and expr == "algorithms":
        args.evaluation[args.n_id] = True
    if member.lower() in INSECURE_MODES and expr == "modes":
        args.triggers.add("unsafemode")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
