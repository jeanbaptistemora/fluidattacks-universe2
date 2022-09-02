from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

INSECURE_HASHES = {"md2", "md4", "md5", "sha1", "sha-1"}


def java_insecure_key(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"].replace('"', "")
        if len(args.triggers) == 0:
            args.triggers.add(member_str)
        else:
            curr_value = next(iter(args.triggers))
            args.triggers.clear()
            args.triggers.add(curr_value + member_str)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def java_insecure_hash(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"]
        if member_str.lower().replace('"', "") in INSECURE_HASHES:
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def java_insecure_cipher(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"].replace('"', "")
        args.triggers.add(member_str)

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
