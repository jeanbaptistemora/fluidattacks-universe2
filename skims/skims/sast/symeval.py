# Standard library
from copy import (
    deepcopy,
)
from itertools import (
    chain,
)
import operator
from typing import (
    Callable,
    Dict,
    Iterator,
    NamedTuple,
    Optional,
    Tuple,
    Union,
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
from sast.common import (
    build_attr_paths,
    DANGER_METHODS_BY_OBJ_ARGS,
    DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION_FINDING,
    DANGER_METHODS_BY_TYPE_AND_VALUE_FINDING,
    DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION,
    DANGER_METHODS_STATIC_SIDE_EFFECTS_FINDING,
    DANGER_METHODS_BY_ARGS_PROPAGATION,
    DANGER_METHODS_BY_OBJ,
    DANGER_METHODS_BY_OBJ_NO_TYPE_ARGS_PROPAGATION_FIDING,
    DANGER_METHODS_BY_TYPE,
    DANGER_METHODS_STATIC_FINDING,
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


class ImpossiblePath(StopEvaluation):
    pass


class EvaluatorArgs(NamedTuple):
    dependencies: graph_model.SyntaxSteps
    finding: core_model.FindingEnum
    graph_db: graph_model.GraphDB
    shard: graph_model.GraphShard
    n_id_next: graph_model.NId
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


def lookup_java_class(
    args: EvaluatorArgs,
    class_name: str,
) -> Optional[graph_model.GraphShardMetadataJavaClass]:
    # First lookup the class in the current shard
    for class_path, class_data in args.shard.metadata.java.classes.items():
        qualified = args.shard.metadata.java.package + class_path

        if qualified.endswith(f'.{class_name}'):
            return class_data

    return None


def lookup_java_method(
    args: EvaluatorArgs,
    method_name: str,
) -> Optional[graph_model.GraphShardMetadataJavaClassMethod]:
    # First lookup the class in the current shard
    for class_path, class_data in args.shard.metadata.java.classes.items():
        for method_path, method_data in class_data.methods.items():
            qualified = \
                args.shard.metadata.java.package + class_path + method_path

            if qualified.endswith(f'.{method_name}'):
                return method_data

    return None


def eval_method(
    args: EvaluatorArgs,
    method_n_id: graph_model.NId,
    method_arguments: graph_model.SyntaxSteps,
) -> Optional[graph_model.SyntaxStep]:
    for syntax_steps in get_possible_syntax_steps_for_n_id(
        args.graph_db,
        finding=args.finding,
        n_id=method_n_id,
        overriden_syntax_steps=list(reversed(method_arguments)),
        shard=args.shard,
    ).values():
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

    # Return a default value
    return None


def syntax_step_assignment(args: EvaluatorArgs) -> None:
    args_danger = any(dep.meta.danger for dep in args.dependencies)
    if not args.syntax_step.meta.danger:
        args.syntax_step.meta.danger = args_danger


def syntax_step_binary_expression(args: EvaluatorArgs) -> None:
    left, right = args.dependencies

    args.syntax_step.meta.danger = left.meta.danger or right.meta.danger

    if left.meta.value is not None and right.meta.value is not None:
        args.syntax_step.meta.value = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '<': operator.lt,
            '<=': operator.le,
            '==': operator.eq,
            '!=': operator.ne,
            '>': operator.gt,
            '>=': operator.ge,
        }.get(args.syntax_step.operator, lambda _, __: None)(
            left.meta.value,
            right.meta.value,
        )


def syntax_step_unary_expression(args: EvaluatorArgs) -> None:
    src, = args.dependencies

    args.syntax_step.meta.danger = src.meta.danger


def syntax_step_declaration(args: EvaluatorArgs) -> None:
    _syntax_step_declaration_danger(args)
    _syntax_step_declaration_values(args)


def _syntax_step_declaration_danger(args: EvaluatorArgs) -> None:
    # Analyze the arguments involved in the assignment
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    # Analyze if the binding itself is sensitive
    no_trust_findings = {
        core_model.FindingEnum.F001_JAVA_SQL,
        core_model.FindingEnum.F004,
        core_model.FindingEnum.F042,
        core_model.FindingEnum.F063_PATH_TRAVERSAL,
    }
    bind_danger = any((
        args.finding in no_trust_findings and any((
            args.syntax_step.var_type in build_attr_paths(
                'javax', 'servlet', 'http', 'HttpServletRequest'
            ),
        )),
    ))

    # Local context
    args.syntax_step.meta.danger = bind_danger or args_danger


def _syntax_step_declaration_values(args: EvaluatorArgs) -> None:
    if len(args.dependencies) == 1:
        args.syntax_step.meta.value = args.dependencies[0].meta.value


def syntax_step_if(args: EvaluatorArgs) -> None:
    predicate, = args.dependencies

    if args.n_id_next and ((
        predicate.meta.value is True
        and args.n_id_next != args.syntax_step.n_id_true
    ) or (
        predicate.meta.value is False
        and args.n_id_next != args.syntax_step.n_id_false
    )):
        # We are walking a path that should not happen
        raise ImpossiblePath()


def syntax_step_switch_label(args: EvaluatorArgs) -> None:
    pred, *cases = args.dependencies

    # We don't know the value of the predicate so let's stop here
    if pred.meta.value is None:
        return

    switch_n_id_next = None

    # Follow every `case X:` in search of the next_id
    for case in cases:
        if isinstance(case, graph_model.SyntaxStepSwitchLabelCase):
            if case.meta.value == pred.meta.value:
                switch_n_id_next = case.meta.n_id
                break

    # Follow every `default:` in search of the next_id
    if switch_n_id_next is None:
        for case in cases:
            if isinstance(case, graph_model.SyntaxStepSwitchLabelDefault):
                switch_n_id_next = case.meta.n_id
                break

    if switch_n_id_next is not None and args.n_id_next != switch_n_id_next:
        # We are walking a path that should not happen
        raise ImpossiblePath()


def syntax_step_switch_label_case(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.value = args.dependencies[0].meta.value


def syntax_step_switch_label_default(_args: EvaluatorArgs) -> None:
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
    args.syntax_step.meta.danger = any(
        dep.meta.danger for dep in args.dependencies
    )
    if len(args.dependencies) == 1:
        args.syntax_step.meta.value = args.dependencies[0].meta.value


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

    danger_methods = DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION_FINDING.get(
        args.finding.name, {})
    if (method_path in danger_methods.get(
            method_var_decl_type, {}) and args_danger):
        args.syntax_step.meta.danger = True


def _analyze_method_static_side_effects(
    args: EvaluatorArgs,
    method: str,
) -> None:
    # functions that make its parameters vulnerable
    if method in DANGER_METHODS_STATIC_SIDE_EFFECTS_FINDING.get(
            args.finding.name, set()):
        for dep in args.dependencies:
            dep.meta.danger = True


def _analyze_method_invocation(args: EvaluatorArgs, method: str) -> None:
    # Analyze the arguments involved in the method invocation
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    method_var, method_path = split_on_first_dot(method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)
    method_var_state = lookup_var_state_by_name(args, method_var)
    method_var_decl_type = (
        method_var_decl.var_type_base if method_var_decl else ''
    )

    args.syntax_step.meta.danger = (
        # Known function to return user controlled data
        method_path in DANGER_METHODS_BY_TYPE.get(method_var_decl_type, {})
    ) or (
        # Know functions that propagate danger if object is dangerous
        method_path in DANGER_METHODS_BY_OBJ.get(method_var_decl_type, {})
        and method_var_state
        and method_var_state.meta.danger
    ) or (
        # Know functions that propagate danger if args are dangerous
        method_path in DANGER_METHODS_BY_OBJ_ARGS.get(method_var_decl_type, {})
        and args_danger
    ) or (
        # Known functions that propagate args danger
        method in DANGER_METHODS_BY_ARGS_PROPAGATION
        and args_danger
    ) or (
        # Known static functions that no require args danger
        method in DANGER_METHODS_STATIC_FINDING.get(
            args.finding.name,
            set(),
        )
    ) or (
        # functions for which the type of the variable cannot be obtained,
        # but which propagate args danger
        method_path
        and method_path in
        DANGER_METHODS_BY_OBJ_NO_TYPE_ARGS_PROPAGATION_FIDING.get(
            args.finding.name, str())
        and args_danger
    )
    _analyze_method_static_side_effects(args, method)
    _analyze_method_by_type_args_propagation(args, method)
    _analyze_method_by_type_args_propagation_side_effects(args, method)

    # function calls with parameters that make the object vulnerable
    if methods := DANGER_METHODS_BY_TYPE_AND_VALUE_FINDING.get(
            args.finding.name,
            dict(),
    ).get(method_var_decl_type):
        parameters = {param.meta.value for param in args.dependencies}
        if (
            parameters.issubset(methods.get(method_path, set()))
            and method_var_decl
        ):
            method_var_decl.meta.danger = True


def _analyze_method_invocation_values(args: EvaluatorArgs) -> None:
    method_var, method_path = split_on_first_dot(args.syntax_step.method)

    if dcl := lookup_var_state_by_name(args, method_var):
        if isinstance(dcl.meta.value, dict):
            _analyze_method_invocation_values_dict(args, dcl, method_path)
        if isinstance(dcl.meta.value, str):
            _analyze_method_invocation_values_str(args, dcl, method_path)
        if isinstance(dcl.meta.value, list):
            _analyze_method_invocation_values_list(args, dcl, method_path)
    elif method := lookup_java_method(args, args.syntax_step.method):
        if return_step := eval_method(args, method.n_id, args.dependencies):
            args.syntax_step.meta.danger = return_step.meta.danger
            args.syntax_step.meta.value = return_step.meta.value


def _analyze_method_invocation_values_dict(
    args: EvaluatorArgs,
    dcl: graph_model.SyntaxStep,
    method_path: str,
) -> None:
    if method_path == 'put':
        value, key = args.dependencies
        dcl.meta.value[key.meta.value] = value
    elif method_path == 'get':
        key = args.dependencies[0]
        args.syntax_step.meta.value = dcl.meta.value.get(key.meta.value)
        args.syntax_step.meta.danger = (
            dcl.meta.value[key.meta.value].meta.danger
            if key.meta.value in dcl.meta.value
            else False
        )


def _analyze_method_invocation_values_str(
    args: EvaluatorArgs,
    dcl: graph_model.SyntaxStep,
    method_path: str,
) -> None:
    if method_path == 'charAt':
        index = int(args.dependencies[0].meta.value)
        args.syntax_step.meta.value = dcl.meta.value[index]


def _analyze_method_invocation_values_list(
    args: EvaluatorArgs,
    dcl: graph_model.SyntaxStep,
    method_path: str,
) -> None:
    if method_path == 'add':
        dcl.meta.value.append(args.dependencies[0])
    elif method_path == 'remove':
        index = int(args.dependencies[0].meta.value)
        dcl.meta.value.pop(index)
    elif method_path == 'get':
        index = int(args.dependencies[0].meta.value)
        args.syntax_step.meta.value = dcl.meta.value[index]
        args.syntax_step.meta.danger = dcl.meta.value[index].meta.danger


def syntax_step_method_invocation(args: EvaluatorArgs) -> None:
    # Analyze if the method itself is untrusted
    method = args.syntax_step.method

    _analyze_method_invocation(args, method)
    _analyze_method_invocation_values(args)


def syntax_step_method_invocation_chain(args: EvaluatorArgs) -> None:
    *method_arguments, parent = args.dependencies

    if isinstance(parent.meta.value, graph_model.GraphShardMetadataJavaClass):
        if args.syntax_step.method in parent.meta.value.methods:
            method = parent.meta.value.methods[args.syntax_step.method]
            if return_step := eval_method(args, method.n_id, method_arguments):
                args.syntax_step.meta.danger = return_step.meta.danger
                args.syntax_step.meta.value = return_step.meta.value
    elif isinstance(parent, graph_model.SyntaxStepMethodInvocation):
        method = parent.method + args.syntax_step.method
        _analyze_method_invocation(args, method)
    elif isinstance(parent, graph_model.SyntaxStepObjectInstantiation):
        method = parent.object_type + args.syntax_step.method
        _analyze_method_invocation(args, method)


def syntax_step_no_op(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = False


def syntax_step_object_instantiation(args: EvaluatorArgs) -> None:
    _syntax_step_object_instantiation_danger(args)
    _syntax_step_object_instantiation_values(args)


def _syntax_step_object_instantiation_danger(args: EvaluatorArgs) -> None:
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
        args.syntax_step.object_type in {
            'java', 'lang', 'StringBuilder',
        },
    ))

    instantiation_danger_no_args = any((
        args.finding == core_model.FindingEnum.F008 and any((
            args.syntax_step.object_type in build_attr_paths(
                'org', 'owasp', 'benchmark', 'helpers', 'SeparateClassRequest'
            ),
        )),
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


def _syntax_step_object_instantiation_values(args: EvaluatorArgs) -> None:
    object_type: str = args.syntax_step.object_type

    if object_type in build_attr_paths('java', 'util', 'ArrayList'):
        args.syntax_step.meta.value = []
    elif object_type in build_attr_paths('java', 'util', 'HashMap'):
        args.syntax_step.meta.value = {}
    elif java_class := lookup_java_class(args, object_type):
        args.syntax_step.meta.value = java_class


def syntax_step_symbol_lookup(args: EvaluatorArgs) -> None:
    if dcl := lookup_var_state_by_name(args, args.syntax_step.symbol):
        # Found it!
        args.syntax_step.meta.danger = dcl.meta.danger
        args.syntax_step.meta.value = dcl.meta.value


def syntax_step_return(args: EvaluatorArgs) -> None:
    returned, = args.dependencies
    args.syntax_step.meta.danger = returned.meta.danger
    args.syntax_step.meta.value = returned.meta.value


def syntax_step_ternary(args: EvaluatorArgs) -> None:
    predicate, left, right = args.dependencies

    if predicate.meta.value is True:
        args.syntax_step.meta.danger = left.meta.danger
        args.syntax_step.meta.value = left.meta.value
    elif predicate.meta.value is False:
        args.syntax_step.meta.danger = right.meta.danger
        args.syntax_step.meta.value = right.meta.value
    elif predicate.meta.value is None:
        args.syntax_step.meta.danger = left.meta.danger or right.meta.danger
    else:
        raise NotImplementedError(predicate.meta.value)


def syntax_step_cast_expression(args: EvaluatorArgs) -> None:
    args.syntax_step.meta.danger = any(
        dep.meta.danger for dep in args.dependencies
    )
    if len(args.dependencies) == 1:
        args.syntax_step.meta.value = args.dependencies[0].meta.value


def syntax_step_instanceof_expression(args: EvaluatorArgs) -> None:
    if isinstance(args.dependencies[0], graph_model.SyntaxStepSymbolLookup):
        if var_declaration := lookup_var_dcl_by_name(
            args,
            args.dependencies[0].symbol,
        ):
            args.syntax_step.meta.value = (
                var_declaration.var_type == args.syntax_step.instanceof_type
            )


EVALUATORS: Dict[object, Evaluator] = {
    graph_model.SyntaxStepAssignment: syntax_step_assignment,
    graph_model.SyntaxStepArrayAccess: syntax_step_array_access,
    graph_model.SyntaxStepArrayInitialization:
    syntax_step_array_initialization,
    graph_model.SyntaxStepArrayInstantiation:
    syntax_step_array_instantiation,
    graph_model.SyntaxStepBinaryExpression: syntax_step_binary_expression,
    graph_model.SyntaxStepCastExpression: syntax_step_cast_expression,
    graph_model.SyntaxStepCatchClause: syntax_step_catch_clause,
    graph_model.SyntaxStepUnaryExpression: syntax_step_unary_expression,
    graph_model.SyntaxStepParenthesizedExpression:
    syntax_step_parenthesized_expression,
    graph_model.SyntaxStepDeclaration: syntax_step_declaration,
    graph_model.SyntaxStepFor: syntax_step_for,
    graph_model.SyntaxStepIf: syntax_step_if,
    graph_model.SyntaxStepInstanceofExpression:
    syntax_step_instanceof_expression,
    graph_model.SyntaxStepSwitch: syntax_step_switch_label,
    graph_model.SyntaxStepSwitchLabelCase: syntax_step_switch_label_case,
    graph_model.SyntaxStepSwitchLabelDefault: syntax_step_switch_label_default,
    graph_model.SyntaxStepLiteral: syntax_step_literal,
    graph_model.SyntaxStepMethodInvocation: syntax_step_method_invocation,
    graph_model.SyntaxStepMethodInvocationChain:
    syntax_step_method_invocation_chain,
    graph_model.SyntaxStepNoOp: syntax_step_no_op,
    graph_model.SyntaxStepObjectInstantiation:
    syntax_step_object_instantiation,
    graph_model.SyntaxStepReturn: syntax_step_return,
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

    syntax_step_index = len(syntax_steps) + 2 * len(overriden_syntax_steps)
    syntax_steps.extend(chain(
        deepcopy(shard.syntax[n_id])[:len(overriden_syntax_steps)],
        deepcopy(overriden_syntax_steps),
        deepcopy(shard.syntax[n_id])[len(overriden_syntax_steps):],
    ))

    while syntax_step_index < len(syntax_steps):
        syntax_step = syntax_steps[syntax_step_index]
        syntax_step_type = type(syntax_step)
        if evaluator := EVALUATORS.get(syntax_step_type):
            evaluator(EvaluatorArgs(
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


@trace()
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


@trace()
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


@trace()
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
        for untrusted_n_id in shard.metadata.nodes.untrusted[finding.name]
    }

    return syntax_steps_map


@trace()
def get_possible_syntax_steps(
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
        output = get_debug_path(f'tree-sitter-syntax-steps-{finding.name}')
        with open(f'{output}.json', 'w') as handle:
            json_dump(syntax_steps_map, handle, indent=2, sort_keys=True)

    return syntax_steps_map


class PossibleSyntaxStepLinear(NamedTuple):
    shard_path: str
    syntax_steps: graph_model.SyntaxSteps
    untrusted_n_id: graph_model.NId


@trace()
def get_possible_syntax_steps_linear(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> Iterator[PossibleSyntaxStepLinear]:
    yield from (
        PossibleSyntaxStepLinear(
            shard_path=shard_path,
            syntax_steps=syntax_steps,
            untrusted_n_id=untrusted_n_id,
        )
        for shard_path, syntax_steps_for_finding in (
            get_possible_syntax_steps(graph_db, finding).items()
        )
        for untrusted_n_id, syntax_steps_for_untrusted_n_id in (
            syntax_steps_for_finding.items()
        )
        for syntax_steps in syntax_steps_for_untrusted_n_id.values()
    )
