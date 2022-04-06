from copy import (
    deepcopy,
)
from ctx import (
    CTX,
)
from itertools import (
    chain,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model as g_m,
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
    method_declaration,
    method_invocation,
    method_invocation_chain,
    no_op,
    object_instantiation,
    parenthesized_expression,
    prefix_expression,
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
    Union,
)
from utils import (
    graph as g,
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
    method_n_id: g_m.NId,
    method_arguments: g_m.SyntaxSteps,
    shard: g_m.GraphShard,
    class_name: str,
) -> JavaClassInstance:
    current_instance = JavaClassInstance(fields={}, class_name=class_name)
    possible_syntax_steps = get_possible_syntax_steps_for_n_id(
        args.shard_db,
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
            if (
                isinstance(syntax_step, g_m.SyntaxStepMethodInvocation)
                and (
                    syntax_step.method.startswith("this.")
                    or "." not in syntax_step.method
                )
                and syntax_step.current_instance
            ):
                current_instance.fields.update(
                    syntax_step.current_instance.fields,
                )

    return current_instance


def eval_method(
    args: EvaluatorArgs,
    method_n_id: g_m.NId,
    method_arguments: g_m.SyntaxSteps,
    shard: g_m.GraphShard,
    current_instance: Optional[JavaClassInstance] = None,
) -> Optional[g_m.SyntaxStep]:
    possible_syntax_steps = get_possible_syntax_steps_for_n_id(
        args.shard_db,
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
                isinstance(syntax_step, g_m.SyntaxStepReturn)
                and syntax_step.meta.danger
            ):
                return syntax_step

    for syntax_steps in possible_syntax_steps.values():
        for syntax_step in reversed(syntax_steps):
            # If none of them match attempt to return the one that has value
            if (
                isinstance(syntax_step, g_m.SyntaxStepReturn)
                and syntax_step.meta.value is not None
            ):
                return syntax_step

    # If non of them match return whatever one
    for syntax_steps in possible_syntax_steps.values():
        for syntax_step in reversed(syntax_steps):
            if isinstance(syntax_step, g_m.SyntaxStepReturn):
                return syntax_step

    # Return a default value
    return None


EVALUATORS: Dict[object, Evaluator] = {
    g_m.SyntaxStepAssignment: assignment.evaluate,
    g_m.SyntaxStepArrayAccess: array_access.evaluate,
    g_m.SyntaxStepArrayInitialization: array_initialization.evaluate,
    g_m.SyntaxStepArrayInstantiation: array_instantiation.evaluate,
    g_m.SyntaxStepAttributeAccess: attribute_access.evaluate,
    g_m.SyntaxStepBinaryExpression: binary_expression.evaluate,
    g_m.SyntaxStepCastExpression: cast_expression.evaluate,
    g_m.SyntaxStepCatchClause: no_op.evaluate,
    g_m.SyntaxStepUnaryExpression: unary_expression.evaluate,
    g_m.SyntaxStepParenthesizedExpression: (parenthesized_expression.evaluate),
    g_m.SyntaxStepDeclaration: declaration.evaluate,
    g_m.SyntaxStepLoop: loop.evaluate,
    g_m.SyntaxStepIf: if_.evaluate,
    g_m.SyntaxStepInstanceofExpression: instanceof_expression.evaluate,
    g_m.SyntaxStepMemberAccessExpression: (member_access_expression.evaluate),
    g_m.SyntaxStepMethodDeclaration: method_declaration.evaluate,
    g_m.SyntaxStepSwitch: switch_label.evaluate,
    g_m.SyntaxStepSwitchLabelCase: switch_label_case.evaluate,
    g_m.SyntaxStepSwitchLabelDefault: no_op.evaluate,
    g_m.SyntaxStepLiteral: literal.evaluate,
    g_m.SyntaxStepMethodInvocation: method_invocation.evaluate,
    g_m.SyntaxStepMethodInvocationChain: (method_invocation_chain.evaluate),
    g_m.SyntaxStepNoOp: no_op.evaluate,
    g_m.SyntaxStepObjectInstantiation: object_instantiation.evaluate,
    g_m.SyntaxStepPrefixExpression: prefix_expression.evaluate,
    g_m.SyntaxStepReturn: return_.evaluate,
    g_m.SyntaxStepSymbolLookup: symbol_lookup.evaluate,
    g_m.SyntaxStepTernary: ternary.evaluate,
    g_m.SyntaxStepThis: no_op.evaluate,
    g_m.SyntaxStepLambdaExpression: lambda_expression.evaluate,
    g_m.SyntaxStepTemplateString: template_string.evaluate,
    g_m.SyntaxStepSubscriptExpression: subscript_expression.evaluate,
}


def eval_syntax_steps(
    shard_db: ShardDb,
    graph_db: g_m.GraphDB,
    *,
    finding: core_model.FindingEnum,
    overriden_syntax_steps: g_m.SyntaxSteps,
    shard: g_m.GraphShard,
    syntax_steps: g_m.SyntaxSteps,
    n_id: g_m.NId,
    n_id_next: g_m.NId,
    current_instance: Optional[
        Union[g_m.CurrentInstance, JavaClassInstance]
    ] = None,
) -> g_m.SyntaxSteps:
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
                    shard_db=shard_db,
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


def _has_already_evaluated(syntax_steps: g_m.SyntaxSteps, n_id: str) -> bool:
    for step in reversed(syntax_steps):
        if n_id == step.meta.n_id:
            return True

    return False


def get_possible_syntax_steps_from_path(
    shard_db: ShardDb,
    graph_db: g_m.GraphDB,
    *,
    finding: core_model.FindingEnum,
    overriden_syntax_steps: g_m.SyntaxSteps,
    shard: g_m.GraphShard,
    path: Tuple[str, ...],
    current_instance: Optional[
        Union[g_m.CurrentInstance, JavaClassInstance]
    ] = None,
) -> g_m.SyntaxSteps:
    syntax_steps: g_m.SyntaxSteps = []

    path_next = padnone(path)
    next(path_next)

    for first, _, (n_id, n_id_next) in mark_ends(zip(path, path_next)):
        try:
            # a node can be part of the cfg but also an argument of
            # a superior node creating duplicates
            if syntax_steps and _has_already_evaluated(syntax_steps, n_id):
                continue
            eval_syntax_steps(
                shard_db=shard_db,
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
    shard_db: ShardDb,
    graph_db: g_m.GraphDB,
    finding: core_model.FindingEnum,
    shard: g_m.GraphShard,
    path_str: str,
) -> g_m.SyntaxSteps:
    syntax_steps: g_m.SyntaxSteps = []

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
                shard_db=shard_db,
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


PossibleSyntaxStepsForUntrustedNId = Dict[str, g_m.SyntaxSteps]
PossibleSyntaxStepsForFinding = Dict[str, PossibleSyntaxStepsForUntrustedNId]
PossibleSyntaxSteps = Dict[str, PossibleSyntaxStepsForFinding]


def get_possible_syntax_steps_from_multiple_go_files(
    shard_db: ShardDb,
    graph_db: g_m.GraphDB,
    shard: g_m.GraphShard,
    n_id: g_m.NId,
    finding: core_model.FindingEnum,
) -> PossibleSyntaxStepsForUntrustedNId:

    # Filter imported packages or modules from the same package that
    # have sink functions related to the finding in question
    imports = shard.metadata.go.imports if shard.metadata.go else []
    functions_of_interest: Dict[str, Tuple[int, List[g_m.SinkFunctions]]] = {
        _shard.metadata.go.package: (
            idx,
            _shard.metadata.go.sink_functions[finding.name],
        )
        for idx, _shard in enumerate(graph_db.shards)
        if (
            _shard != shard
            and _shard.metadata.go
            and (
                _shard.metadata.go.package in imports
                or dirname(shard.path) == dirname(_shard.path)
            )
            and finding.name in _shard.metadata.go.sink_functions
        )
    }
    # Build the way the functions are called in the analyzed code
    current_package = str(
        shard.metadata.go.package if shard.metadata.go else None
    )
    calls_of_interest: Dict[str, Tuple[int, g_m.SinkFunctions]] = {
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
    methods_called: Dict[str, Tuple[int, g_m.SinkFunctions]] = {
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
            shard_db,
            graph_db,
            finding=finding,
            shard=shard,
            path_str=path,
        )
        for path in paths
    }


def get_possible_syntax_steps_for_n_id(
    shard_db: ShardDb,
    graph_db: g_m.GraphDB,
    *,
    finding: core_model.FindingEnum,
    n_id: g_m.NId,
    overriden_syntax_steps: Optional[g_m.SyntaxSteps] = None,
    shard: g_m.GraphShard,
    current_instance: Optional[
        Union[g_m.CurrentInstance, JavaClassInstance]
    ] = None,
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
            shard_db,
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

    if shard.metadata.language == g_m.GraphShardMetadataLanguage.GO:
        syntax_steps_map.update(
            get_possible_syntax_steps_from_multiple_go_files(
                shard_db=shard_db,
                graph_db=graph_db,
                shard=shard,
                n_id=n_id,
                finding=finding,
            )
        )

    return syntax_steps_map


def get_possible_syntax_steps_for_finding(
    shard_db: ShardDb,
    graph_db: g_m.GraphDB,
    finding: core_model.FindingEnum,
    shard: g_m.GraphShard,
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
        shard.metadata.language == g_m.GraphShardMetadataLanguage.JAVASCRIPT
    ) and inputs:
        syntax_steps_map = {
            "1": get_possible_syntax_steps_for_n_id(
                shard_db,
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
                shard_db,
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
    shard_db: ShardDb,
    graph_db: g_m.GraphDB,
    finding: core_model.FindingEnum,
) -> PossibleSyntaxSteps:
    syntax_steps_map: PossibleSyntaxSteps = {
        shard.path: get_possible_syntax_steps_for_finding(
            shard_db=shard_db,
            graph_db=graph_db,
            finding=finding,
            shard=shard,
        )
        for shard in graph_db.shards
    }

    if CTX.debug:
        output = get_debug_path(f"tree-sitter-syntax-steps-{finding.name}")
        with open(f"{output}.json", "w", encoding="utf-8") as handle:
            json_dump(syntax_steps_map, handle, indent=2, sort_keys=True)

    return syntax_steps_map
