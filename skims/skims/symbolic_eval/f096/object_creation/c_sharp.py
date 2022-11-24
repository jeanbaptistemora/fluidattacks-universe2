from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_js_deserialization(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] == "SimpleTypeResolver":
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def cs_xml_serial(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] == "HttpRequest":
        args.evaluation[args.n_id] = True
        args.triggers.add("HttpRequest")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
