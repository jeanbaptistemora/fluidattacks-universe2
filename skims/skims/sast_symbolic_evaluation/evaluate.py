from copy import (
    deepcopy,
)
from itertools import (
    chain,
)
from model import (
    core_model,
    graph_model,
)
from more_itertools import (
    mark_ends,
    padnone,
)
from os.path import (
    dirname,
)
from sast_symbolic_evaluation.cases import (
    array_access,
    array_initialization,
    array_instantiation,
    assignment,
    attribute_access,
    binary_expression,
    cast_expression,
    declaration,
    if_,
    instanceof_expression,
    lambda_expression,
    literal,
    loop,
    member_access_expression,
    method_invocation,
    method_invocation_chain,
    no_op,
    object_instantiation,
    parenthesized_expression,
    return_,
    subscript_expression,
    switch_label,
    switch_label_case,
    symbol_lookup,
    template_string,
    ternary,
    unary_expression,
)
from sast_symbolic_evaluation.types import (
    Evaluator,
    EvaluatorArgs,
    ImpossiblePath,
    JavaClassInstance,
    StopEvaluation,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)
from utils import (
    graph as g,
)
from utils.ctx import (
    CTX,
)
from utils.encodings import (
    json_dump,
)
from utils.logs import (
    log_blocking,
    log_exception_blocking,
)
from utils.string import (
    get_debug_path,
)


def eval_constructor(
    args: EvaluatorArgs,
    method_n_id: graph_model.NId,
    method_arguments: graph_model.SyntaxSteps,
    shard: graph_model.GraphShard,
    class_name: str,
) -> JavaClassInstance:
    current_instance = JavaClassInstance(fields={}, class_name=class_name)
    possible_syntax_steps = get_possible_syntax_steps_for_n_id(
        args.graph_db,
        finding=args.finding,
        n_id=method_n_id,
        overriden_syntax_steps=list(reversed(method_arguments)),
        shard=shard,
        current_instance=current_instance,
    )

    for syntax_steps in possible_syntax_steps.values():
        # Check modified fields
        for syntax_step in syntax_steps:
            if isinstance(
                syntax_step, graph_model.SyntaxStepMethodInvocation
            ) and (
                syntax_step.method.startswith("this.")
                or "." not in syntax_step.method
            ):
                current_instance.fields.update(
                    syntax_step.current_instance.fields,
                )

    return current_instance


def eval_method(
    args: EvaluatorArgs,
    method_n_id: graph_model.NId,
    method_arguments: graph_model.SyntaxSteps,
    shard: graph_model.GraphShard,
    current_instance: Optional[JavaClassInstance] = None,
) -> Optional[graph_model.SyntaxStep]:
    possible_syntax_steps = get_possible_syntax_steps_for_n_id(
        args.graph_db,
        finding=args.finding,
        n_id=method_n_id,
        overriden_syntax_steps=list(reversed(method_arguments)),
        shard=shard,
        current_instance=current_instance,
    )

    for syntax_steps in possible_syntax_steps.values():
        for syntax_step in reversed(syntax_steps):
            # Attempt to return the dangerous syntax step
            if (
                isinstance(syntax_step, graph_model.SyntaxStepReturn)
                and syntax_step.meta.danger
            ):
                return syntax_step

    for syntax_steps in possible_syntax_steps.values():
        for syntax_step in reversed(syntax_steps):
            # If none of them match attempt to return the one that has value
            if (
                isinstance(syntax_step, graph_model.SyntaxStepReturn)
                and syntax_step.meta.value is not None
            ):
                return syntax_step

    # If non of them match return whatever one
    for syntax_steps in possible_syntax_steps.values():
        for syntax_step in reversed(syntax_steps):
            if isinstance(syntax_step, graph_model.SyntaxStepReturn):
                return syntax_step

    # Return a default value
    return None


EVALUATORS: Dict[object, Evaluator] = {
    graph_model.SyntaxStepAssignment: assignment.evaluate,
    graph_model.SyntaxStepArrayAccess: array_access.evaluate,
    graph_model.SyntaxStepArrayInitialization: array_initialization.evaluate,
    graph_model.SyntaxStepArrayInstantiation: array_instantiation.evaluate,
    graph_model.SyntaxStepAttributeAccess: attribute_access.evaluate,
    graph_model.SyntaxStepBinaryExpression: binary_expression.evaluate,
    graph_model.SyntaxStepCastExpression: cast_expression.evaluate,
    graph_model.SyntaxStepCatchClause: no_op.evaluate,
    graph_model.SyntaxStepUnaryExpression: unary_expression.evaluate,
    graph_model.SyntaxStepParenthesizedExpression: (
        parenthesized_expression.evaluate
    ),
    graph_model.SyntaxStepDeclaration: declaration.evaluate,
    graph_model.SyntaxStepLoop: loop.evaluate,
    graph_model.SyntaxStepIf: if_.evaluate,
    graph_model.SyntaxStepInstanceofExpression: instanceof_expression.evaluate,
    graph_model.SyntaxStepMemberAccessExpression: (
        member_access_expression.evaluate
    ),
    graph_model.SyntaxStepSwitch: switch_label.evaluate,
    graph_model.SyntaxStepSwitchLabelCase: switch_label_case.evaluate,
    graph_model.SyntaxStepSwitchLabelDefault: no_op.evaluate,
    graph_model.SyntaxStepLiteral: literal.evaluate,
    graph_model.SyntaxStepMethodInvocation: method_invocation.evaluate,
    graph_model.SyntaxStepMethodInvocationChain: (
        method_invocation_chain.evaluate
    ),
    graph_model.SyntaxStepNoOp: no_op.evaluate,
    graph_model.SyntaxStepObjectInstantiation: object_instantiation.evaluate,
    graph_model.SyntaxStepReturn: return_.evaluate,
    graph_model.SyntaxStepSymbolLookup: symbol_lookup.evaluate,
    graph_model.SyntaxStepTernary: ternary.evaluate,
    graph_model.SyntaxStepThis: no_op.evaluate,
    graph_model.SyntaxStepLambdaExpression: lambda_expression.evaluate,
    graph_model.SyntaxStepTemplateString: template_string.evaluate,
    graph_model.SyntaxStepSubscriptExpression: subscript_expression.evaluate,
}


def eval_syntax_steps(
    graph_db: graph_model.GraphDB,
    *,
    finding: core_model.FindingEnum,
    overriden_syntax_steps: graph_model.SyntaxSteps,
    shard: graph_model.GraphShard,
    syntax_steps: graph_model.SyntaxSteps,
    n_id: graph_model.NId,
    n_id_next: graph_model.NId,
    current_instance: Optional[graph_model.CurrentInstance] = None,
) -> graph_model.SyntaxSteps:
    if n_id not in shard.syntax:
        # We were not able to fully understand this node syntax
        raise StopEvaluation(f"Missing Syntax Reader, {shard.path} @ {n_id}")

    # Append the syntax steps from this node
    syntax_step_index = len(syntax_steps)
    syntax_steps.extend(deepcopy(shard.syntax[n_id]))

    # If any, override the initial syntax steps
    # This can be used to "pass" parameters to functions
    for syntax_step, overriden_syntax_step in zip(
        syntax_steps[syntax_step_index:],
        overriden_syntax_steps,
    ):
        syntax_step.meta.danger = overriden_syntax_step.meta.danger
        syntax_step.meta.value = overriden_syntax_step.meta.value

    # Skip evaluating the overriden syntax steps
    syntax_step_index += len(overriden_syntax_steps)

    while syntax_step_index < len(syntax_steps):
        syntax_step = syntax_steps[syntax_step_index]
        syntax_step_type = type(syntax_step)
        if evaluator := EVALUATORS.get(syntax_step_type):
            evaluator(
                EvaluatorArgs(
                    eval_method=eval_method,
                    eval_constructor=eval_constructor,
                    dependencies=get_dependencies(
                        syntax_step_index, syntax_steps
                    ),
                    finding=finding,
                    graph_db=graph_db,
                    shard=shard,
                    n_id_next=n_id_next,
                    syntax_step=syntax_step,
                    syntax_step_index=syntax_step_index,
                    syntax_steps=syntax_steps,
                    current_instance=current_instance,
                )
            )
        else:
            # We are not able to evaluate this step
            raise StopEvaluation(f"Missing evaluator, {syntax_step_type}")

        syntax_step_index += 1

    return syntax_steps


def _has_already_evaluated(
    syntax_steps: graph_model.SyntaxSteps, n_id: str
) -> bool:
    for step in reversed(syntax_steps):
        if n_id == step.meta.n_id:
            return True

    return False


def get_possible_syntax_steps_from_path(
    graph_db: graph_model.GraphDB,
    *,
    finding: core_model.FindingEnum,
    overriden_syntax_steps: graph_model.SyntaxSteps,
    shard: graph_model.GraphShard,
    path: Tuple[str, ...],
    current_instance: Optional[graph_model.CurrentInstance] = None,
) -> graph_model.SyntaxSteps:
    syntax_steps: graph_model.SyntaxSteps = []

    path_next = padnone(path)
    next(path_next)

    for first, _, (n_id, n_id_next) in mark_ends(zip(path, path_next)):
        try:
            # a node can be part of the cfg but also an argument of
            # a superior node creating duplicates
            if syntax_steps and _has_already_evaluated(syntax_steps, n_id):
                continue
            eval_syntax_steps(
                graph_db=graph_db,
                finding=finding,
                overriden_syntax_steps=overriden_syntax_steps if first else [],
                shard=shard,
                syntax_steps=syntax_steps,
                n_id=n_id,
                n_id_next=n_id_next,
                current_instance=current_instance,
            )
        except ImpossiblePath:
            return []
        except StopEvaluation as exc:
            log_exception_blocking("debug", exc)
            return syntax_steps

    return syntax_steps


def get_possible_syntax_steps_from_path_str_multiple_files(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    path_str: str,
) -> graph_model.SyntaxSteps:
    syntax_steps: graph_model.SyntaxSteps = []

    # The paths have syntax 'node-node-node--shard--node-node...'
    # Split the syntax to know which nodes and which shard we are currently
    # interested in
    path_split: List[str] = path_str.split("--")
    switch_shard_map: Dict[int, str] = {}
    if len(path_split) > 1:
        switch_shard_map = {
            len(path_split[idx - 1].split("-")): val
            for idx, val in enumerate(path_split)
            if idx % 2 != 0
        }
    path: Tuple[str, ...] = tuple(
        chain.from_iterable(
            [
                val.split("-")
                for idx, val in enumerate(path_split)
                if idx % 2 == 0
            ]
        )
    )
    path_next = padnone(path)
    next(path_next)

    for idx, (n_id, n_id_next) in enumerate(zip(path, path_next)):
        if idx in switch_shard_map:
            shard_idx = graph_db.shards_by_path[switch_shard_map[idx]]
            shard = graph_db.shards[shard_idx]
        try:
            eval_syntax_steps(
                graph_db=graph_db,
                finding=finding,
                overriden_syntax_steps=[],
                shard=shard,
                syntax_steps=syntax_steps,
                n_id=n_id,
                n_id_next=n_id_next,
                current_instance=None,
            )
        except ImpossiblePath:
            return []
        except StopEvaluation as exc:
            log_exception_blocking("debug", exc)
            return syntax_steps

    return syntax_steps


PossibleSyntaxStepsForUntrustedNId = Dict[str, graph_model.SyntaxSteps]
PossibleSyntaxStepsForFinding = Dict[str, PossibleSyntaxStepsForUntrustedNId]
PossibleSyntaxSteps = Dict[str, PossibleSyntaxStepsForFinding]


def get_possible_syntax_steps_from_multiple_go_files(
    graph_db: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    n_id: graph_model.NId,
    finding: core_model.FindingEnum,
) -> PossibleSyntaxStepsForUntrustedNId:

    # Filter imported packages or modules from the same package that
    # have sink functions related to the finding in question
    imports = shard.metadata.go.imports
    functions_of_interest: Dict[
        str, Tuple[int, List[graph_model.SinkFunctions]]
    ] = {
        _shard.metadata.go.package: (
            idx,
            _shard.metadata.go.sink_functions[finding.name],
        )
        for idx, _shard in enumerate(graph_db.shards)
        if (
            _shard != shard
            and (
                _shard.metadata.go.package in imports
                or dirname(shard.path) == dirname(_shard.path)
            )
            and finding.name in _shard.metadata.go.sink_functions
        )
    }
    # Build the way the functions are called in the analyzed code
    current_package = shard.metadata.go.package
    calls_of_interest: Dict[str, Tuple[int, graph_model.SinkFunctions]] = {
        f"{pkg}.{fn.name}" if pkg != current_package else fn.name: (_shard, fn)
        for pkg, (_shard, fns) in functions_of_interest.items()
        for fn in fns
    }

    graph = shard.graph
    syntax = shard.syntax
    cfg_p_id = g.lookup_first_cfg_parent(graph, n_id)
    fn_calls_n_ids = tuple(
        c_id
        for c_id in g.filter_nodes(
            graph,
            (cfg_p_id,) + g.adj_cfg(graph, cfg_p_id, depth=-1),
            g.pred_has_labels(label_type="call_expression"),
        )
        # This condition is temporal until all syntax cases are supported
        if c_id in syntax
    )
    # Link the node where the function is called with the shard and information
    # where the function is declared
    methods_called: Dict[str, Tuple[int, graph_model.SinkFunctions]] = {
        fn_call_n_id: calls_of_interest[syntax_step.method]
        for fn_call_n_id in fn_calls_n_ids
        for syntax_step in syntax[fn_call_n_id]
        if (
            syntax_step.type == "SyntaxStepMethodInvocation"
            and syntax_step.method in calls_of_interest
        )
    }

    # Calculate the paths that the CFG follows
    paths = tuple(
        "-".join(path + (f"-{graph_db.shards[shard_idx].path}-",) + ext_path)
        for c_id, (shard_idx, fn) in methods_called.items()
        for path in g.paths(graph, cfg_p_id, c_id, label_cfg="CFG")
        for ext_path in g.paths(
            graph_db.shards[shard_idx].graph,
            fn.n_id,
            fn.s_id,
            label_cfg="CFG",
        )
    )
    return {
        path: get_possible_syntax_steps_from_path_str_multiple_files(
            graph_db,
            finding=finding,
            shard=shard,
            path_str=path,
        )
        for path in paths
    }


def get_possible_syntax_steps_for_n_id(
    graph_db: graph_model.GraphDB,
    *,
    finding: core_model.FindingEnum,
    n_id: graph_model.NId,
    overriden_syntax_steps: Optional[graph_model.SyntaxSteps] = None,
    shard: graph_model.GraphShard,
    current_instance: Optional[graph_model.CurrentInstance] = None,
    only_sinks: bool = False,
) -> PossibleSyntaxStepsForUntrustedNId:
    log_blocking(
        "info",
        "Evaluating %s, shard %s, node %s",
        finding.name,
        shard.path,
        n_id,
    )

    syntax_steps_map: PossibleSyntaxStepsForUntrustedNId = {
        # Path identifier -> syntax_steps
        "-".join(path): get_possible_syntax_steps_from_path(
            graph_db,
            finding=finding,
            overriden_syntax_steps=overriden_syntax_steps or [],
            shard=shard,
            path=path,
            current_instance=current_instance,
        )
        for path in g.branches_cfg(
            graph=shard.graph,
            only_sinks=only_sinks,
            n_id=g.lookup_first_cfg_parent(shard.graph, n_id),
            finding=finding,
        )
    }

    if shard.metadata.language == graph_model.GraphShardMetadataLanguage.GO:
        syntax_steps_map.update(
            get_possible_syntax_steps_from_multiple_go_files(
                graph_db=graph_db, shard=shard, n_id=n_id, finding=finding
            )
        )

    return syntax_steps_map


def get_possible_syntax_steps_for_finding(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
) -> PossibleSyntaxStepsForFinding:
    syntax_steps_map: PossibleSyntaxStepsForFinding = {}
    inputs = [
        n_id
        for n_id in shard.graph.nodes
        if "label_input_type" in shard.graph.nodes[n_id]
        if any(
            core_model.FINDING_ENUM_FROM_STR[label] == finding
            for label in shard.graph.nodes[n_id]["label_input_type"]
        )
    ]
    if (
        shard.metadata.language
        == graph_model.GraphShardMetadataLanguage.JAVASCRIPT
    ) and inputs:
        syntax_steps_map = {
            "1": get_possible_syntax_steps_for_n_id(
                graph_db,
                finding=finding,
                n_id="1",
                shard=shard,
                only_sinks=True,
            )
        }
    else:
        syntax_steps_map = {
            untrusted_n_id: get_possible_syntax_steps_for_n_id(
                graph_db,
                finding=finding,
                n_id=untrusted_n_id,
                shard=shard,
                only_sinks=True,
            )
            for untrusted_n_id in inputs
        }

    return syntax_steps_map


def get_all_possible_syntax_steps(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> PossibleSyntaxSteps:
    syntax_steps_map: PossibleSyntaxSteps = {
        shard.path: get_possible_syntax_steps_for_finding(
            graph_db=graph_db,
            finding=finding,
            shard=shard,
        )
        for shard in graph_db.shards
    }

    if CTX.debug:
        output = get_debug_path(f"tree-sitter-syntax-steps-{finding.name}")
        with open(f"{output}.json", "w") as handle:
            json_dump(syntax_steps_map, handle, indent=2, sort_keys=True)

    return syntax_steps_map
