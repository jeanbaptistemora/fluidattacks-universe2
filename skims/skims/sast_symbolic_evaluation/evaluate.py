# Standard library
from copy import (
    deepcopy,
)
from typing import (
    Dict,
    Iterator,
    NamedTuple,
    Optional,
    Tuple,
)

# Third party libraries
from more_itertools import (
    mark_ends,
    padnone,
)

# Local libraries
from model import (
    core_model,
    graph_model,
)
from sast_symbolic_evaluation.cases import (
    array_access,
    array_initialization,
    array_instantiation,
    assignment,
    binary_expression,
    cast_expression,
    declaration,
    if_,
    instanceof_expression,
    literal,
    method_invocation_chain,
    method_invocation,
    no_op,
    object_instantiation,
    parenthesized_expression,
    return_,
    switch_label_case,
    switch_label,
    symbol_lookup,
    ternary,
    unary_expression,
)
from sast_symbolic_evaluation.types import (
    Evaluator,
    EvaluatorArgs,
    ImpossiblePath,
    StopEvaluation,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
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
)
from utils.string import (
    get_debug_path,
    split_on_last_dot,
)


def eval_constructor(
    args: EvaluatorArgs,
    method_n_id: graph_model.NId,
    method_arguments: graph_model.SyntaxSteps,
    shard: graph_model.GraphShard,
) -> Dict[str, Optional[graph_model.SyntaxStep]]:
    possible_syntax_steps = get_possible_syntax_steps_for_n_id(
        args.graph_db,
        finding=args.finding,
        n_id=method_n_id,
        overriden_syntax_steps=list(reversed(method_arguments)),
        shard=shard,
    )
    modified_fields = {}
    for syntax_steps in possible_syntax_steps.values():
        # Check modified fields
        for syntax_step in syntax_steps:
            if (
                isinstance(syntax_step, graph_model.SyntaxStepAssignment)
                and syntax_step.var.startswith('this.')
            ):
                _, field = split_on_last_dot(syntax_step.var)
                modified_fields[field] = syntax_step.meta.value

    return modified_fields


def eval_method(
    args: EvaluatorArgs,
    method_n_id: graph_model.NId,
    method_arguments: graph_model.SyntaxSteps,
    shard: graph_model.GraphShard,
) -> Optional[graph_model.SyntaxStep]:
    possible_syntax_steps = get_possible_syntax_steps_for_n_id(
        args.graph_db,
        finding=args.finding,
        n_id=method_n_id,
        overriden_syntax_steps=list(reversed(method_arguments)),
        shard=shard,
    )

    for syntax_steps in possible_syntax_steps.values():
        # Attempt to return the dangerous syntax step
        for syntax_step in reversed(syntax_steps):
            if (
                isinstance(syntax_step, graph_model.SyntaxStepReturn)
                and syntax_step.meta.danger
            ):
                return syntax_step

        # If none of them match attempt to return the one that has value
        for syntax_step in reversed(syntax_steps):
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
    graph_model.SyntaxStepAssignment:
    assignment.evaluate,
    graph_model.SyntaxStepArrayAccess:
    array_access.evaluate,
    graph_model.SyntaxStepArrayInitialization:
    array_initialization.evaluate,
    graph_model.SyntaxStepArrayInstantiation:
    array_instantiation.evaluate,
    graph_model.SyntaxStepBinaryExpression:
    binary_expression.evaluate,
    graph_model.SyntaxStepCastExpression:
    cast_expression.evaluate,
    graph_model.SyntaxStepCatchClause:
    no_op.evaluate,
    graph_model.SyntaxStepUnaryExpression:
    unary_expression.evaluate,
    graph_model.SyntaxStepParenthesizedExpression:
    parenthesized_expression.evaluate,
    graph_model.SyntaxStepDeclaration:
    declaration.evaluate,
    graph_model.SyntaxStepFor:
    no_op.evaluate,
    graph_model.SyntaxStepIf:
    if_.evaluate,
    graph_model.SyntaxStepInstanceofExpression:
    instanceof_expression.evaluate,
    graph_model.SyntaxStepSwitch:
    switch_label.evaluate,
    graph_model.SyntaxStepSwitchLabelCase:
    switch_label_case.evaluate,
    graph_model.SyntaxStepSwitchLabelDefault:
    no_op.evaluate,
    graph_model.SyntaxStepLiteral:
    literal.evaluate,
    graph_model.SyntaxStepMethodInvocation:
    method_invocation.evaluate,
    graph_model.SyntaxStepMethodInvocationChain:
    method_invocation_chain.evaluate,
    graph_model.SyntaxStepNoOp:
    no_op.evaluate,
    graph_model.SyntaxStepObjectInstantiation:
    object_instantiation.evaluate,
    graph_model.SyntaxStepReturn:
    return_.evaluate,
    graph_model.SyntaxStepSymbolLookup:
    symbol_lookup.evaluate,
    graph_model.SyntaxStepTernary:
    ternary.evaluate,
    graph_model.SyntaxStepThis:
    no_op.evaluate,
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
) -> graph_model.SyntaxSteps:
    if n_id not in shard.syntax:
        # We were not able to fully understand this node syntax
        raise StopEvaluation(f'Missing Syntax Reader, {shard.path} @ {n_id}')

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
            evaluator(EvaluatorArgs(
                eval_method=eval_method,
                eval_constructor=eval_constructor,
                dependencies=get_dependencies(syntax_step_index, syntax_steps),
                finding=finding,
                graph_db=graph_db,
                shard=shard,
                n_id_next=n_id_next,
                syntax_step=syntax_step,
                syntax_step_index=syntax_step_index,
                syntax_steps=syntax_steps,
            ))
        else:
            # We are not able to evaluate this step
            raise StopEvaluation(f'Missing evaluator, {syntax_step_type}')

        syntax_step_index += 1

    return syntax_steps


def get_possible_syntax_steps_from_path(
    graph_db: graph_model.GraphDB,
    *,
    finding: core_model.FindingEnum,
    overriden_syntax_steps: graph_model.SyntaxSteps,
    shard: graph_model.GraphShard,
    path: Tuple[str, ...],
) -> graph_model.SyntaxSteps:
    syntax_steps: graph_model.SyntaxSteps = []

    path_next = padnone(path)
    next(path_next)

    for first, _, (n_id, n_id_next) in mark_ends(zip(path, path_next)):
        try:
            eval_syntax_steps(
                graph_db=graph_db,
                finding=finding,
                overriden_syntax_steps=overriden_syntax_steps if first else [],
                shard=shard,
                syntax_steps=syntax_steps,
                n_id=n_id,
                n_id_next=n_id_next,
            )
        except ImpossiblePath:
            return []
        except StopEvaluation as exc:
            log_blocking('debug', str(exc))
            return syntax_steps

    return syntax_steps


PossibleSyntaxStepsForUntrustedNId = Dict[str, graph_model.SyntaxSteps]
PossibleSyntaxStepsForFinding = Dict[str, PossibleSyntaxStepsForUntrustedNId]
PossibleSyntaxSteps = Dict[str, PossibleSyntaxStepsForFinding]


def get_possible_syntax_steps_for_n_id(
    graph_db: graph_model.GraphDB,
    *,
    finding: core_model.FindingEnum,
    n_id: graph_model.NId,
    overriden_syntax_steps: Optional[graph_model.SyntaxSteps] = None,
    shard: graph_model.GraphShard,
) -> PossibleSyntaxStepsForUntrustedNId:
    syntax_steps_map: PossibleSyntaxStepsForUntrustedNId = {
        # Path identifier -> syntax_steps
        '-'.join(path): get_possible_syntax_steps_from_path(
            graph_db,
            finding=finding,
            overriden_syntax_steps=overriden_syntax_steps or [],
            shard=shard,
            path=path,
        )
        for path in g.branches_cfg(
            graph=shard.graph,
            n_id=g.lookup_first_cfg_parent(shard.graph, n_id),
            finding=finding
        )
    }

    return syntax_steps_map


def get_possible_syntax_steps_for_finding(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
) -> PossibleSyntaxStepsForFinding:
    syntax_steps_map: PossibleSyntaxStepsForFinding = {
        untrusted_n_id: get_possible_syntax_steps_for_n_id(
            graph_db,
            finding=finding,
            n_id=untrusted_n_id,
            shard=shard,
        )
        for untrusted_n_id in shard.graph.nodes
        if 'label_input_type' in shard.graph.nodes[untrusted_n_id]
        if any(
            core_model.FINDING_ENUM_FROM_STR[label] == finding
            for label in shard.graph.nodes[untrusted_n_id]['label_input_type']
        )
    }

    return syntax_steps_map


def get_possible_syntax_steps(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> PossibleSyntaxSteps:
    syntax_steps_map: PossibleSyntaxSteps = {}
    for shard_index, shard in enumerate(graph_db.shards):
        log_blocking(
            'info', 'Evaluating %s, shard %s: %s',
            finding.name, shard_index, shard.path,
        )

        syntax_steps_map[shard.path] = get_possible_syntax_steps_for_finding(
            graph_db=graph_db,
            finding=finding,
            shard=shard,
        )

    if CTX.debug:
        output = get_debug_path(f'tree-sitter-syntax-steps-{finding.name}')
        with open(f'{output}.json', 'w') as handle:
            json_dump(syntax_steps_map, handle, indent=2, sort_keys=True)

    return syntax_steps_map


class PossibleSyntaxStepLinear(NamedTuple):
    finding: core_model.FindingEnum
    shard_path: str
    syntax_steps: graph_model.SyntaxSteps


def get_possible_syntax_steps_linear(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> Iterator[PossibleSyntaxStepLinear]:
    yield from (
        PossibleSyntaxStepLinear(
            finding=finding,
            shard_path=shard_path,
            syntax_steps=syntax_steps,
        )
        for shard_path, syntax_steps_for_finding in (
            get_possible_syntax_steps(graph_db, finding).items()
        )
        for syntax_steps_for_n_id in syntax_steps_for_finding.values()
        for syntax_steps in syntax_steps_for_n_id.values()
    )
