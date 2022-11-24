from model.graph_model import (
    SyntaxStepAttributeAccess,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    GoParsedFloat,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from typing import (
    cast,
)


def check_go_float_sanitization(args: EvaluatorArgs) -> bool:
    for method, attr in {
        "math.IsNaN": "is_nan",
        "math.IsInf": "is_inf",
    }.items():
        if args.syntax_step.method == method:
            for dep in args.dependencies:
                if isinstance(dep.meta.value, GoParsedFloat):
                    setattr(dep.meta.value, attr, False)
                    dep.meta.danger = (
                        dep.meta.value.is_inf or dep.meta.value.is_nan
                    )
                    if not dep.meta.danger and isinstance(
                        dep, SyntaxStepAttributeAccess
                    ):
                        parent = get_dependencies(
                            args.syntax_step_index - 1, args.syntax_steps
                        )[0]
                        parent.meta.value[dep.attribute] = dep.meta
            return True
    return False


def attempt_go_parse_float(args: EvaluatorArgs) -> bool:
    if args.syntax_step.method == "strconv.ParseFloat":
        args.syntax_step.meta.value = GoParsedFloat(
            method_n_id=args.syntax_step.meta.n_id,
            shard_idx=args.graph_db.shards.index(args.shard),
        )
        args.syntax_step.meta.danger = True
        return True

    if check_go_float_sanitization(args):
        return True

    # Avoids reporting the vulnerability in the line where the dangerous value
    # is used, since it can be far from the point where the real danger was
    # injected
    if args.shard.graph.nodes[args.syntax_step.meta.n_id].get(
        "label_sink_type"
    ):
        for dep in args.dependencies:
            if isinstance(dep.meta.value, GoParsedFloat) and dep.meta.danger:
                dep.meta.danger = False

                # Add a sink label to the method's node so the report is made
                # on the line the danger is inserted instead of the line where
                # the dangerous value is used
                shard_idx = cast(int, dep.meta.value.shard_idx)
                n_id = dep.meta.value.method_n_id
                graph = args.graph_db.shards[shard_idx].graph
                if "label_sink_type" in graph.nodes[n_id]:
                    graph.nodes[n_id]["label_sink_type"].add(args.finding.name)
                else:
                    graph.nodes[n_id]["label_sink_type"] = {args.finding.name}
    return False
