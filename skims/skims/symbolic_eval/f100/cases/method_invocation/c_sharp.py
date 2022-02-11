from symbolic_eval.types import (
    SymbolicEvalArgs,
)


def evaluate(args: SymbolicEvalArgs) -> bool:
    mi_attrs = args.graph.nodes[args.n_id]

    al_id = mi_attrs.get("arguments_id")
    al_danger = args.evaluation[al_id] if al_id is not None else False

    if mi_attrs["expression"] == "WebRequest.Create" and al_danger:
        args.evaluation[args.n_id] = True
    else:
        args.evaluation[args.n_id] = False

    return args.evaluation[args.n_id]
