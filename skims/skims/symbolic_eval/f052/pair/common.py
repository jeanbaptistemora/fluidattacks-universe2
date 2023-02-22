from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def insecure_mode(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    key = n_attrs["key_id"]
    value = n_attrs["value_id"]
    if args.graph.nodes[key].get("symbol") == "mode":
        val_danger = args.generic(args.fork(n_id=value)).danger
        if val_danger:
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def insecure_key_pair(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    key = n_attrs["key_id"]
    value = n_attrs["value_id"]
    key_name = args.graph.nodes[key].get("symbol")

    if key_name and key_name.lower() == "moduluslength":
        if args.generic(args.fork(n_id=value)).danger:
            args.evaluation[args.n_id] = True
            args.triggers.add("unsafemodulus")

    if key_name and key_name.lower() == "namedcurve":
        if args.generic(args.fork(n_id=value)).danger:
            args.evaluation[args.n_id] = True
            args.triggers.add("unsafecurve")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def insecure_sign(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    nodes = args.graph.nodes
    key_id = nodes[args.n_id].get("key_id")
    value_id = nodes[args.n_id].get("value_id")

    if (nodes[key_id].get("label_type") == "SymbolLookup") and (
        nodes[key_id].get("symbol").lower() == "algorithm"
        and (label_type := nodes[value_id].get("label_type"))
    ):
        if (label_type == "Literal") and (
            nodes[value_id].get("value").lower()[1:-1] == "hs256"
        ):
            args.triggers.add(args.n_id)
        elif label_type == "SymbolLookup" and (
            symbol := nodes[value_id].get("symbol")
        ):
            args.triggers.add(f"{symbol}_{value_id}")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def insecure_sign_async(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    nodes = args.graph.nodes
    key_id = nodes[args.n_id].get("key_id")
    value_id = nodes[args.n_id].get("value_id")

    if (
        (nodes[key_id].get("label_type") == "SymbolLookup")
        and (nodes[key_id].get("symbol").lower() == "alg")
        and (label_type := nodes[value_id].get("label_type"))
        and (label_type == "Literal")
        and (nodes[value_id].get("value").lower()[1:-1] == "hs256")
    ):
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
