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
    Union,
)

# Local libraries
from model import (
    core_model,
    graph_model,
)
from sast.common import (
    build_attr_paths,
    DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION,
    DANGER_METHODS_STATIC_SIDE_EFFECTS,
    DANGER_METHODS_BY_ARGS_PROPAGATION,
    DANGER_METHODS_BY_OBJ,
    DANGER_METHODS_BY_OBJ_NO_TYPE_ARGS_PROPAGATION,
    DANGER_METHODS_BY_TYPE,
    DANGER_METHODS_STATIC,
    split_on_first_dot,
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
from utils.function import (
    trace,
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
    finding: core_model.FindingEnum
    syntax_step: graph_model.SyntaxStep
    syntax_step_index: int
    syntax_steps: graph_model.SyntaxSteps


Evaluator = Callable[[EvaluatorArgs], None]


def lookup_vars(
    args: EvaluatorArgs,
) -> Iterator[Union[
    graph_model.SyntaxStepAssignment,
    graph_model.SyntaxStepDeclaration,
    graph_model.SyntaxStepSymbolLookup,
]]:
    for syntax_step in reversed(args.syntax_steps[0:args.syntax_step_index]):
        if isinstance(syntax_step, (
            graph_model.SyntaxStepAssignment,
            graph_model.SyntaxStepDeclaration,
            graph_model.SyntaxStepSymbolLookup,
        )):
            yield syntax_step


def lookup_var_dcl_by_name(
    args: EvaluatorArgs,
    var_name: str,
) -> Optional[Union[graph_model.SyntaxStepDeclaration,
                    graph_model.SyntaxStepSymbolLookup]]:

    vars_lookup = list(var for var in lookup_vars(args)
                       if isinstance(var, (
                           graph_model.SyntaxStepDeclaration,
                           graph_model.SyntaxStepSymbolLookup,
                       )))
    for syntax_step in vars_lookup:
        if isinstance(syntax_step, graph_model.SyntaxStepDeclaration
                      ) and syntax_step.var == var_name:
            return syntax_step
        # SyntaxStepDeclaration may not be vulnerable, but a later assignment
        # may be vulnerable
        if isinstance(syntax_step, graph_model.SyntaxStepSymbolLookup
                      ) and syntax_step.symbol == var_name:
            for var in vars_lookup:
                if isinstance(var, graph_model.SyntaxStepDeclaration
                              ):
                    if var.var == var_name:
                        return graph_model.SyntaxStepDeclaration(
                            meta=syntax_step.meta,
                            var=var.var,
                            var_type=var.var_type)
    return None


def lookup_var_state_by_name(
    args: EvaluatorArgs,
    var_name: str,
) -> Optional[Union[
    graph_model.SyntaxStepAssignment,
    graph_model.SyntaxStepDeclaration,
    graph_model.SyntaxStepSymbolLookup,
]]:
    for syntax_step in lookup_vars(args):
        if (isinstance(syntax_step, (
                graph_model.SyntaxStepDeclaration,
                graph_model.SyntaxStepAssignment,
        )) and syntax_step.var == var_name) or (
                isinstance(syntax_step, graph_model.SyntaxStepSymbolLookup)
                and syntax_step.symbol == var_name):
            return syntax_step
    return None


def syntax_step_assignment(args: EvaluatorArgs) -> None:
    args_danger = any(dep.meta.danger for dep in args.dependencies)
    if not args.syntax_step.meta.danger:
        args.syntax_step.meta.danger = args_danger


def syntax_step_binary_expression(args: EvaluatorArgs) -> None:
    left, right = args.dependencies

    args.syntax_step.meta.danger = left.meta.danger or right.meta.danger


def syntax_step_unary_expression(args: EvaluatorArgs) -> None:
    src, = args.dependencies

    args.syntax_step.meta.danger = src.meta.danger


def syntax_step_declaration(args: EvaluatorArgs) -> None:
    # Analyze the arguments involved in the assignment
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    # Analyze if the binding itself is sensitive
    bind_danger = any((
        args.finding in core_model.ALLOW_UNTRUSTED_NODES and any((
            args.syntax_step.var_type in build_attr_paths(
                'javax', 'servlet', 'http', 'HttpServletRequest'
            ),
        )),
        args.finding == core_model.FindingEnum.F034 and any((
            args.syntax_step.var_type in build_attr_paths(
                'javax', 'servlet', 'http', 'Cookie'
            ),
        )) and args_danger,
    ))

    # Local context
    args.syntax_step.meta.danger = bind_danger or args_danger


def syntax_step_if(_args: EvaluatorArgs) -> None:
    pass


def syntax_step_switch(_args: EvaluatorArgs) -> None:
    pass


def syntax_step_for(_args: EvaluatorArgs) -> None:
    pass


def syntax_step_catch_clause(_args: EvaluatorArgs) -> None:
    pass


def syntax_step_array_access(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = args.dependencies[1].meta.danger


def syntax_step_array_initialization(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = any(dep.meta.danger
                                       for dep in args.dependencies)


def syntax_step_array_instantiation(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = any(dep.meta.danger
                                       for dep in args.dependencies)


def syntax_step_parenthesized_expression(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = any(dep.meta.danger
                                       for dep in args.dependencies)


def syntax_step_literal(args: EvaluatorArgs) -> None:
    if args.syntax_step.value_type in {
        'boolean',
        'null',
    }:
        args.syntax_step.meta.value = {
            'false': False,
            'null': None,
            'true': True,
        }[args.syntax_step.value]
    elif args.syntax_step.value_type == 'number':
        args.syntax_step.meta.value = float(args.syntax_step.value)
    elif args.syntax_step.value_type == 'string':
        args.syntax_step.meta.value = args.syntax_step.value
    else:
        raise NotImplementedError()


def _analyze_method_by_type_args_propagation_side_effects(
    args: EvaluatorArgs,
    method: str,
) -> None:
    # Functions that when called make the parent object vulnerable
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    method_var, method_path = split_on_first_dot(method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)
    method_var_decl_type = (method_var_decl.var_type_base
                            if method_var_decl else '')

    if (method_path in DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION.get(
            method_var_decl_type, {}) and args_danger):
        if method_var_decl:
            method_var_decl.meta.danger = True


def _analyze_method_by_type_args_propagation(
    args: EvaluatorArgs,
    method: str,
) -> None:
    # Functions that when called make the parent object vulnerable
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    method_var, method_path = split_on_first_dot(method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)
    method_var_decl_type = (method_var_decl.var_type_base
                            if method_var_decl else '')

    if (method_path in DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION.get(
            method_var_decl_type, {}) and args_danger):
        args.syntax_step.meta.danger = True


def _analyze_method_static_side_effects(
    args: EvaluatorArgs,
    method: str,
) -> None:
    # functions that make its parameters vulnerable
    if method in DANGER_METHODS_STATIC_SIDE_EFFECTS:
        for dep in args.dependencies:
            dep.meta.danger = True


def _analyze_method_invocation(args: EvaluatorArgs, method: str) -> None:
    # Analyze the arguments involved in the method invocation
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    method_var, method_path = split_on_first_dot(method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)
    method_var_decl_type = (
        method_var_decl.var_type_base if method_var_decl else ''
    )

    args.syntax_step.meta.danger = (
        # Known function to return user controlled data
        method_path in DANGER_METHODS_BY_TYPE.get(method_var_decl_type, {})
    ) or (
        # Know functions that propagate danger if object is dangerous
        method_path in DANGER_METHODS_BY_OBJ.get(method_var_decl_type, {})
        and method_var_decl
        and method_var_decl.meta.danger
    ) or (
        # Known functions that propagate args danger
        method in DANGER_METHODS_BY_ARGS_PROPAGATION
        and args_danger
    ) or (
        # Known static functions that no require args danger
        method in DANGER_METHODS_STATIC
    ) or (
        # functions for which the type of the variable cannot be obtained,
        # but which propagate args danger
        method_path in DANGER_METHODS_BY_OBJ_NO_TYPE_ARGS_PROPAGATION
        and args_danger
    )
    _analyze_method_static_side_effects(args, method)
    _analyze_method_by_type_args_propagation(args, method)
    _analyze_method_by_type_args_propagation_side_effects(args, method)


def syntax_step_method_invocation(args: EvaluatorArgs) -> None:
    # Analyze if the method itself is untrusted
    method = args.syntax_step.method

    _analyze_method_invocation(args, method)


def syntax_step_method_invocation_chain(args: EvaluatorArgs) -> None:
    method = args.syntax_step.method
    parent: Optional[graph_model.SyntaxStepMethodInvocation] = None

    for dep in args.dependencies:
        if isinstance(dep, (
                graph_model.SyntaxStepMethodInvocation,
                graph_model.SyntaxStepObjectInstantiation,
        )):
            parent = dep
    if not parent:
        return None

    if isinstance(parent, graph_model.SyntaxStepMethodInvocation):
        method = parent.method + method
    elif isinstance(parent, graph_model.SyntaxStepObjectInstantiation):
        method = parent.object_type + method
    _analyze_method_invocation(args, method)
    return None


def syntax_step_no_op(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = False


def syntax_step_object_instantiation(args: EvaluatorArgs) -> None:
    # Analyze the arguments involved in the instantiation
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    # Analyze if the object being instantiated is dangerous
    instantiation_danger = any((
        args.finding == core_model.FindingEnum.F063_PATH_TRAVERSAL and any((
            args.syntax_step.object_type in build_attr_paths(
                'java', 'io', 'File'
            ),
            args.syntax_step.object_type in build_attr_paths(
                'java', 'io', 'FileInputStream'
            ),
            args.syntax_step.object_type in build_attr_paths(
                'java', 'io', 'FileOutputStream'
            ),
        )),
        args.finding == core_model.FindingEnum.F004 and any((
            args.syntax_step.object_type in build_attr_paths(
                'ProcessBuilder',
            ),
        )),
    ))

    instantiation_danger_no_args = any((
        args.finding == core_model.FindingEnum.F034 and any((
            args.syntax_step.object_type in build_attr_paths(
                'java', 'util', 'Random'
            ),
        )),
    ))
    if instantiation_danger_no_args:
        args.syntax_step.meta.danger = True
    elif instantiation_danger:
        args.syntax_step.meta.danger = args_danger if args else True
    else:
        args.syntax_step.meta.danger = args_danger


def syntax_step_symbol_lookup(args: EvaluatorArgs) -> None:
    if dcl := lookup_var_state_by_name(args, args.syntax_step.symbol):
        # Found it!
        args.syntax_step.meta.danger = dcl.meta.danger
        args.syntax_step.meta.value = dcl.meta.value


def syntax_step_ternary(args: EvaluatorArgs) -> None:
    predicate, left, right = args.dependencies

    if predicate.meta.value is True:
        args.syntax_step.meta.danger = left.meta.danger
    elif predicate.meta.value is False:
        args.syntax_step.meta.danger = right.meta.danger
    elif predicate.meta.value is None:
        args.syntax_step.meta.danger = left.meta.danger or right.meta.danger
    else:
        raise NotImplementedError(predicate.meta.value)


EVALUATORS: Dict[object, Evaluator] = {
    graph_model.SyntaxStepAssignment: syntax_step_assignment,
    graph_model.SyntaxStepArrayAccess: syntax_step_array_access,
    graph_model.SyntaxStepArrayInitialization:
    syntax_step_array_initialization,
    graph_model.SyntaxStepArrayInstantiation:
    syntax_step_array_instantiation,
    graph_model.SyntaxStepBinaryExpression: syntax_step_binary_expression,
    graph_model.SyntaxStepCatchClause: syntax_step_catch_clause,
    graph_model.SyntaxStepUnaryExpression: syntax_step_unary_expression,
    graph_model.SyntaxStepParenthesizedExpression:
    syntax_step_parenthesized_expression,
    graph_model.SyntaxStepDeclaration: syntax_step_declaration,
    graph_model.SyntaxStepFor: syntax_step_for,
    graph_model.SyntaxStepIf: syntax_step_if,
    graph_model.SyntaxStepSwitch: syntax_step_switch,
    graph_model.SyntaxStepLiteral: syntax_step_literal,
    graph_model.SyntaxStepMethodInvocation: syntax_step_method_invocation,
    graph_model.SyntaxStepMethodInvocationChain:
    syntax_step_method_invocation_chain,
    graph_model.SyntaxStepNoOp: syntax_step_no_op,
    graph_model.SyntaxStepObjectInstantiation:
    syntax_step_object_instantiation,
    graph_model.SyntaxStepSymbolLookup: syntax_step_symbol_lookup,
    graph_model.SyntaxStepTernary: syntax_step_ternary,
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
    *,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    syntax_steps: graph_model.SyntaxSteps,
    n_id: graph_model.NId,
) -> graph_model.SyntaxSteps:
    if n_id not in shard.syntax:
        # We were not able to fully understand this node syntax
        raise StopEvaluation(f'Missing Syntax Reader, {shard.path} @ {n_id}')

    syntax_step_index = len(syntax_steps)
    syntax_steps.extend(deepcopy(shard.syntax[n_id]))

    for syntax_step_index, syntax_step in enumerate(
        syntax_steps[syntax_step_index:],
        start=syntax_step_index,
    ):
        syntax_step_type = type(syntax_step)
        if evaluator := EVALUATORS.get(syntax_step_type):
            evaluator(EvaluatorArgs(
                dependencies=get_dependencies(syntax_step_index, syntax_steps),
                finding=finding,
                syntax_step=syntax_step,
                syntax_step_index=syntax_step_index,
                syntax_steps=syntax_steps,
            ))
        else:
            # We are not able to evaluate this step
            raise StopEvaluation(f'Missing evaluator, {syntax_step_type}')

    return syntax_steps


@trace()
def get_possible_syntax_steps_from_path(
    graph_db: graph_model.GraphDB,
    *,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    path: Tuple[str, ...],
) -> graph_model.SyntaxSteps:
    syntax_steps: graph_model.SyntaxSteps = []

    for n_id in path:
        try:
            eval_syntax_steps(
                _=graph_db,
                finding=finding,
                shard=shard,
                syntax_steps=syntax_steps,
                n_id=n_id,
            )
        except StopEvaluation as exc:
            log_blocking('debug', str(exc))
            break

    return syntax_steps


PossibleSyntaxStepsForUntrustedNId = Dict[str, graph_model.SyntaxSteps]
PossibleSyntaxStepsForFinding = Dict[str, PossibleSyntaxStepsForUntrustedNId]
PossibleSyntaxSteps = Dict[str, Dict[str, PossibleSyntaxStepsForFinding]]


@trace()
def get_possible_syntax_steps_for_untrusted_n_id(
    graph_db: graph_model.GraphDB,
    *,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    untrusted_n_id: graph_model.NId,
) -> PossibleSyntaxStepsForUntrustedNId:
    syntax_steps_map: PossibleSyntaxStepsForUntrustedNId = {
        # Path identifier -> syntax_steps
        '-'.join(path): get_possible_syntax_steps_from_path(
            graph_db,
            finding=finding,
            shard=shard,
            path=path,
        )
        for path in g.branches_cfg(
            graph=shard.graph,
            n_id=g.lookup_first_cfg_parent(shard.graph, untrusted_n_id),
            finding=finding
        )
    }

    return syntax_steps_map


@trace()
def get_possible_syntax_steps_for_finding(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
) -> PossibleSyntaxStepsForFinding:
    syntax_steps_map: PossibleSyntaxStepsForFinding = {
        untrusted_n_id: get_possible_syntax_steps_for_untrusted_n_id(
            graph_db,
            finding=finding,
            shard=shard,
            untrusted_n_id=untrusted_n_id,
        )
        for untrusted_n_id in shard.metadata.nodes.untrusted[finding.name]
    }

    return syntax_steps_map


@trace()
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
