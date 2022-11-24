from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_disabled_strong_crypto(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if (
        args.graph.nodes[args.n_id]["value"]
        == '"Switch.System.Net.DontEnableSchUseStrongCrypto"'
    ):
        args.evaluation[args.n_id] = True
        args.triggers.add("Switch.System.Net.DontEnableSchUseStrongCrypto")
    if args.graph.nodes[args.n_id]["value"] == "true":
        args.evaluation[args.n_id] = True
        args.triggers.add("true")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def cs_insecure_keys(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if (
        args.graph.nodes[args.n_id]["value_type"] == "number"
        and int(args.graph.nodes[args.n_id]["value"]) < 2048
    ):
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def cs_rsa_secure_mode(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["value"] == "false":
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
