from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def js_ls_sensitive_data(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if (
        cls_name := args.graph.nodes[args.n_id].get("name")
    ) and cls_name.lower() == "xmlhttprequest":
        args.evaluation[args.n_id] = True
        args.triggers.add("xml_instance")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
