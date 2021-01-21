# Standard library
from copy import (
    deepcopy,
)
from typing import (
    Callable,
    Dict,
    Iterator,
    NamedTuple,
    Optional,
    Tuple,
)

# Local libraries
from model import (
    core_model,
    graph_model,
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
)


class StopEvaluation(Exception):
    pass


class EvaluatorArgs(NamedTuple):
    dependencies: graph_model.SyntaxSteps
    syntax_step: graph_model.SyntaxStep
    syntax_step_index: int
    syntax_steps: graph_model.SyntaxSteps


Evaluator = Callable[[EvaluatorArgs], None]


def lookup_vars(
    args: EvaluatorArgs,
) -> Iterator[graph_model.SyntaxStepDeclaration]:
    for syntax_step in args.syntax_steps[0:args.syntax_step_index]:
        if isinstance(syntax_step, graph_model.SyntaxStepDeclaration):
            yield syntax_step


def lookup_var_by_name(
    args: EvaluatorArgs,
    var_name: str,
) -> Optional[graph_model.SyntaxStepDeclaration]:
    for syntax_step in lookup_vars(args):
        if syntax_step.var == var_name:
            return syntax_step
    return None


def syntax_step_binary_expression(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = False


def syntax_step_declaration(args: EvaluatorArgs) -> None:
    # Analyze the arguments involved in the assignment
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    # Analyze if the binding itself is sensitive
    bind_danger = any((
        # This type is an HTTP request from JavaX framework
        args.syntax_step.var_type == 'HttpServletRequest',
    ))

    # Local context
    args.syntax_step.meta.danger = bind_danger or args_danger


def syntax_step_literal(args: EvaluatorArgs) -> None:
    if args.syntax_step.value_type == 'string':
        args.syntax_step.meta.value = args.syntax_step.value
    else:
        raise NotImplementedError()


def syntax_step_method_invocation(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = False


def syntax_step_no_op(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = False


def syntax_step_object_instantiation(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = False


def syntax_step_symbol_lookup(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = False


EVALUATORS: Dict[object, Evaluator] = {
    graph_model.SyntaxStepBinaryExpression: syntax_step_binary_expression,
    graph_model.SyntaxStepDeclaration: syntax_step_declaration,
    graph_model.SyntaxStepLiteral: syntax_step_literal,
    graph_model.SyntaxStepMethodInvocation: syntax_step_method_invocation,
    graph_model.SyntaxStepNoOp: syntax_step_no_op,
    graph_model.SyntaxStepObjectInstantiation:
    syntax_step_object_instantiation,
    graph_model.SyntaxStepSymbolLookup: syntax_step_symbol_lookup,
}


def get_dependencies(
    syntax_step_index: int,
    syntax_steps: graph_model.SyntaxSteps,
) -> graph_model.SyntaxSteps:
    dependencies: graph_model.SyntaxSteps = []
    dependencies_depth: int = 0
    dependencies_expected_length: int = (
        -syntax_steps[syntax_step_index].meta.dependencies
    )

    while len(dependencies) < dependencies_expected_length:
        syntax_step_index -= 1

        if dependencies_depth:
            dependencies_depth += 1
        else:
            dependencies.append(syntax_steps[syntax_step_index])

        dependencies_depth += syntax_steps[syntax_step_index].meta.dependencies

    return dependencies


def eval_syntax_steps(
    _: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    n_id: graph_model.NId,
) -> graph_model.SyntaxSteps:
    if n_id not in shard.syntax:
        # We were not able to fully understand this node syntax
        raise StopEvaluation(f'Missing Syntax Reader, {shard.path} @ {n_id}')

    syntax_steps = deepcopy(shard.syntax[n_id])

    for syntax_step_index, syntax_step in enumerate(syntax_steps):
        syntax_step_type = type(syntax_step)
        if evaluator := EVALUATORS.get(syntax_step_type):
            evaluator(EvaluatorArgs(
                dependencies=get_dependencies(syntax_step_index, syntax_steps),
                syntax_step=syntax_step,
                syntax_step_index=syntax_step_index,
                syntax_steps=syntax_steps,
            ))
        else:
            # We are not able to evaluate this step
            raise StopEvaluation(f'Missing evaluator, {syntax_step_type}')

    return syntax_steps


def get_possible_syntax_steps_from_path(
    graph_db: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    path: Tuple[str, ...],
) -> graph_model.SyntaxSteps:
    syntax_steps: graph_model.SyntaxSteps = []

    for n_id in path:
        try:
            syntax_steps.extend(eval_syntax_steps(
                _=graph_db,
                shard=shard,
                n_id=n_id,
            ))
        except StopEvaluation as exc:
            log_blocking('debug', str(exc))
            break

    return syntax_steps


PossibleSyntaxStepsForUntrustedNId = Dict[str, graph_model.SyntaxSteps]
PossibleSyntaxStepsForFinding = Dict[str, PossibleSyntaxStepsForUntrustedNId]
PossibleSyntaxSteps = Dict[str, Dict[str, PossibleSyntaxStepsForFinding]]


def get_possible_syntax_steps_for_untrusted_n_id(
    graph_db: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    *,
    untrusted_n_id: graph_model.NId,
) -> PossibleSyntaxStepsForUntrustedNId:
    syntax_steps_map: PossibleSyntaxStepsForUntrustedNId = {
        # Path identifier -> syntax_steps
        '-'.join(path): get_possible_syntax_steps_from_path(
            graph_db, shard, path,
        )
        for path in g.branches_cfg(
            graph=shard.graph,
            n_id=g.lookup_first_cfg_parent(shard.graph, untrusted_n_id),
        )
    }

    return syntax_steps_map


def get_possible_syntax_steps_for_finding(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
) -> PossibleSyntaxStepsForFinding:
    syntax_steps_map: PossibleSyntaxStepsForFinding = {
        untrusted_n_id: get_possible_syntax_steps_for_untrusted_n_id(
            graph_db,
            shard=shard,
            untrusted_n_id=untrusted_n_id,
        )
        for untrusted_n_id in shard.metadata.nodes.untrusted[finding.name]
    }

    return syntax_steps_map


def get_possible_syntax_steps(
    graph_db: graph_model.GraphDB,
) -> PossibleSyntaxSteps:
    syntax_steps_map: PossibleSyntaxSteps = {
        shard.path: {
            finding.name: get_possible_syntax_steps_for_finding(
                graph_db=graph_db,
                finding=finding,
                shard=shard,
            )
            for finding in core_model.FindingEnum
        }
        for shard in graph_db.shards
    }

    if CTX.debug:
        output = get_debug_path('tree-sitter-syntax-steps')
        with open(f'{output}.json', 'w') as handle:
            json_dump(syntax_steps_map, handle, indent=2, sort_keys=True)

    return syntax_steps_map
