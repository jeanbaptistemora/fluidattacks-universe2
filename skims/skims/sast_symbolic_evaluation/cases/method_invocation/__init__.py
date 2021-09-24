from model.graph_model import (
    GraphShardMetadataLanguage,
    SyntaxStep,
    SyntaxStepDeclaration,
    SyntaxStepObjectInstantiation,
    SyntaxStepSymbolLookup,
)
from sast_symbolic_evaluation.cases.method_invocation.constants import (
    BY_ARGS_PROPAGATION,
    BY_OBJ,
    BY_OBJ_ARGS,
    BY_OBJ_NO_TYPE_ARGS_PROPAG,
    BY_TYPE,
    BY_TYPE_AND_VALUE_FINDING,
    BY_TYPE_ARGS_PROPAG_FINDING,
    BY_TYPE_ARGS_PROPAGATION,
    BY_TYPE_HANDLER,
    RETURN_TYPES,
    STATIC_FINDING,
    STATIC_SIDE_EFFECTS,
)
from sast_symbolic_evaluation.cases.method_invocation.go import (
    attempt_go_parse_float,
)
from sast_symbolic_evaluation.cases.method_invocation.java import (
    attempt_java_looked_up_class,
    attempt_java_security_msgdigest,
    attempt_java_util_properties_methods,
    list_add as java_list_add,
    list_remove as java_list_remove,
)
from sast_symbolic_evaluation.cases.method_invocation.javascript import (
    list_concat as javascript_list_concat,
    list_get as javascript_list_get,
    list_pop as javascript_list_pop,
    list_push as javascript_list_push,
    list_shift as javascript_list_shift,
    process as javascript_process,
)
from sast_symbolic_evaluation.lookup import (
    lookup_class,
    lookup_field,
    lookup_method,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    JavaClassInstance,
)
from sast_symbolic_evaluation.utils_generic import (
    lookup_var_dcl_by_name,
    lookup_var_state_by_name,
)
from typing import (
    Optional,
    Union,
)
from utils.string import (
    split_on_first_dot,
    split_on_last_dot,
)


def _propagate_return_type(args: EvaluatorArgs) -> None:
    method = args.syntax_step.method
    method_var, method_path = split_on_first_dot(method)

    # pylint: disable=used-before-assignment
    if (
        method_var
        and (method_var_decl := lookup_var_dcl_by_name(args, method_var))
        and method_var_decl.var_type
        and (
            return_type := RETURN_TYPES.get(
                method_var_decl.var_type, dict()
            ).get(method_path or method_var)
        )
    ):
        args.syntax_step.return_type = return_type


def evaluate(args: EvaluatorArgs) -> None:
    language = args.shard.metadata.language

    if language == GraphShardMetadataLanguage.JAVASCRIPT:
        _propagate_return_type(args)
        javascript_process(args)

    if language == GraphShardMetadataLanguage.GO:
        evaluate_go(args)

    if language in (
        GraphShardMetadataLanguage.JAVA,
        GraphShardMetadataLanguage.JAVASCRIPT,
        GraphShardMetadataLanguage.CSHARP,
    ):
        evaluate_many(args)


def evaluate_go(args: EvaluatorArgs) -> None:
    # pylint: disable=expression-not-assigned
    (attempt_go_parse_float(args) or attempt_the_old_way(args))


def evaluate_many(args: EvaluatorArgs) -> None:
    # pylint: disable=expression-not-assigned
    (
        attempt_java_util_properties_methods(args)
        or attempt_java_security_msgdigest(args)
        or attempt_the_old_way(args)
        or attempt_java_looked_up_class(args)
    )


def attempt_by_args_propagation_no_type(
    args: EvaluatorArgs,
    method: str,
) -> bool:
    _, method_path = split_on_first_dot(method)

    if method_path in BY_OBJ_NO_TYPE_ARGS_PROPAG.get(
        args.finding.name, {}
    ) and any(dep.meta.danger for dep in args.dependencies):
        args.syntax_step.meta.danger = True
        return True

    return False


def attempt_by_args_propagation(args: EvaluatorArgs, method: str) -> bool:
    method_field, method_name = split_on_last_dot(args.syntax_step.method)
    if field := lookup_field(args, method_field):
        method = f"{field.metadata.var_type}.{method_name}"

    if (method in BY_ARGS_PROPAGATION) and any(
        dep.meta.danger for dep in args.dependencies
    ):
        args.syntax_step.meta.danger = True
        return True

    return False


def attempt_by_obj(
    args: EvaluatorArgs,
    method: str,
    method_var_decl: Optional[
        Union[
            SyntaxStepDeclaration,
            SyntaxStepSymbolLookup,
        ]
    ],
) -> bool:
    method_var, method_path = split_on_first_dot(method)

    # pylint: disable=used-before-assignment
    if (
        method_var_decl
        and (
            method_var_decl.var_type_base
            and method_path in BY_OBJ.get(method_var_decl.var_type_base, {})
        )
        and (method_var_state := lookup_var_state_by_name(args, method_var))
        and (method_var_state.meta.danger)
    ):
        args.syntax_step.meta.danger = True
        return True

    return False


def attempt_by_obj_args(
    args: EvaluatorArgs,
    method: str,
    method_var_decl: Optional[
        Union[
            SyntaxStepDeclaration,
            SyntaxStepSymbolLookup,
        ]
    ],
) -> bool:
    _, method_path = split_on_first_dot(method)

    if (
        method_var_decl
        and (
            method_var_decl.var_type_base
            and method_path
            in BY_OBJ_ARGS.get(method_var_decl.var_type_base, {})
        )
        and any(dep.meta.danger for dep in args.dependencies)
    ):
        args.syntax_step.meta.danger = True
        return True

    return False


def attempt_by_type_args_propagation(
    args: EvaluatorArgs,
    method: str,
    method_var_decl: Optional[
        Union[
            SyntaxStepDeclaration,
            SyntaxStepSymbolLookup,
        ]
    ],
) -> bool:
    # Functions that when called make the parent object vulnerable
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    _, method_path = split_on_first_dot(method)

    if args_danger and method_var_decl and method_var_decl.var_type_base:
        if method_path in (
            BY_TYPE_ARGS_PROPAGATION.get(method_var_decl.var_type_base, {})
        ):
            args.syntax_step.meta.danger = True
            method_var_decl.meta.danger = True
            return True

        if method_path in (
            BY_TYPE_ARGS_PROPAG_FINDING.get(args.finding.name, {}).get(
                method_var_decl.var_type_base, {}
            )
        ):
            args.syntax_step.meta.danger = True
            return True

    return False


def attempt_by_type_and_value_finding(
    args: EvaluatorArgs,
    method: str,
    method_var_decl: Optional[
        Union[
            SyntaxStepDeclaration,
            SyntaxStepSymbolLookup,
        ]
    ],
) -> bool:
    # function calls with parameters that make the object vulnerable
    _, method_path = split_on_first_dot(method)

    if (
        method_var_decl
        and method_var_decl.var_type_base
        and (
            methods := (
                BY_TYPE_AND_VALUE_FINDING.get(args.finding.name, {}).get(
                    method_var_decl.var_type_base
                )
            )
        )
    ):
        parameters = {param.meta.value for param in args.dependencies}
        if parameters.issubset(methods.get(method_path, set())):
            method_var_decl.meta.danger = True
            return True

    return False


def attempt_static(args: EvaluatorArgs, method: str) -> bool:
    if method in STATIC_FINDING.get(args.finding.name, {}):
        args.syntax_step.meta.danger = True
        return True
    return False


def attempt_static_side_effects(args: EvaluatorArgs, method: str) -> bool:
    if method in STATIC_SIDE_EFFECTS.get(args.finding.name, {}):
        for dep in args.dependencies:
            dep.meta.danger = True
        return True
    return False


def attempt_by_type(
    args: EvaluatorArgs,
    method: str,
    method_var_decl: Optional[
        Union[
            SyntaxStepDeclaration,
            SyntaxStepSymbolLookup,
        ]
    ],
) -> bool:
    method_var, method_path = split_on_first_dot(method)

    if (
        method_var_decl
        and method_var_decl.var_type_base
        and (method_path in BY_TYPE.get(method_var_decl.var_type_base, {}))
    ):
        args.syntax_step.meta.danger = True
        return True

    if (method_var_decl := lookup_field(args, method_var)) and (
        method_path in BY_TYPE.get(method_var_decl.metadata.var_type, {})
    ):
        args.syntax_step.meta.danger = True
        return True

    return False


def attemp_by_type_handler(
    args: EvaluatorArgs,
    method: str,
    method_var_decl: Optional[
        Union[
            SyntaxStepDeclaration,
            SyntaxStepSymbolLookup,
        ]
    ],
) -> bool:
    _, method_path = split_on_first_dot(method)

    if method_var_decl and method_var_decl.var_type_base:
        var_type = method_var_decl.var_type_base
        if handlers := BY_TYPE_HANDLER.get(var_type, {}).get(method_path):
            for handler in handlers:
                handler(args)
            return True
        base_type, _function = split_on_last_dot(var_type)
        if handlers := BY_TYPE_HANDLER.get(base_type, {}).get(_function):
            for handler in handlers:
                handler(args)
            return True

    return False


def attempt_the_old_way(args: EvaluatorArgs) -> bool:
    # Analyze if the method itself is untrusted
    method = args.syntax_step.method

    analyze_method_invocation(args, method)
    analyze_method_invocation_values(args)

    return False


def analyze_method_invocation(args: EvaluatorArgs, method: str) -> None:
    method_var, _ = split_on_first_dot(method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)
    # pylint: disable=expression-not-assigned,too-many-boolean-expressions
    (
        attempt_static(args, method)
        or attempt_static_side_effects(args, method)
        or attempt_by_args_propagation_no_type(args, method)
        or attempt_by_type_args_propagation(args, method, method_var_decl)
        or attempt_by_obj(args, method, method_var_decl)
        or attempt_by_obj_args(args, method, method_var_decl)
        or attempt_by_type_and_value_finding(args, method, method_var_decl)
        or attempt_by_args_propagation(args, method)
        or attempt_by_type(args, method, method_var_decl)
        or analyze_method_invocation_local(args, method)
        or analyze_method_invocation_external(args, method, method_var_decl)
        or attemp_by_type_handler(args, method, method_var_decl)
    )


def analyze_method_invocation_local(
    args: EvaluatorArgs,
    method: str,
) -> bool:
    method_var, method_path = split_on_first_dot(method)

    if method_var == "this":
        method_name = method_path
    elif not method_path and method_var:
        method_name = method_var
    else:
        return False

    # pylint: disable=used-before-assignment
    if (_method := lookup_method(args, method_name)) and (
        return_step := args.eval_method(
            args,
            _method.metadata.n_id,
            args.dependencies,
            args.graph_db.shards_by_path_f(_method.shard_path),
        )
    ):
        args.syntax_step.meta.danger = return_step.meta.danger
        args.syntax_step.meta.value = return_step.meta.value
        return True

    return False


def analyze_method_invocation_external(
    args: EvaluatorArgs,
    method: str,
    method_var_decl: Optional[
        Union[
            SyntaxStepDeclaration,
            SyntaxStepSymbolLookup,
        ]
    ],
) -> bool:
    _, method_path = split_on_first_dot(method)
    method_var_decl_type = None

    if method_var_decl:
        method_var_decl_type = method_var_decl.var_type
    # lookup methods with teh format new Test().some()
    # last argument is teh instance
    elif (
        args.dependencies
        and isinstance(
            args.dependencies[-1],
            SyntaxStepObjectInstantiation,
        )
        and lookup_class(
            args,
            args.dependencies[-1].object_type,
        )
    ):
        method_var_decl_type = args.dependencies[-1].object_type

    if method_var_decl_type and (
        _method := lookup_method(
            args,
            method_path,
            method_var_decl_type,
        )
    ):
        if args.shard.path != _method.shard_path and (
            return_step := args.eval_method(
                args,
                _method.metadata.n_id,
                args.dependencies,
                args.graph_db.shards_by_path_f(_method.shard_path),
                method_var_decl.meta.value if method_var_decl else None,
            )
        ):
            args.syntax_step.meta.danger = return_step.meta.danger
            args.syntax_step.meta.value = return_step.meta.value
            return True

    return False


def analyze_method_invocation_values(
    args: EvaluatorArgs,
    method: Optional[str] = None,
) -> None:
    method = method or args.syntax_step.method
    method_var, method_path = split_on_first_dot(method)
    method_var_decl_type = None
    # lookup methods with teh format new Test().some()
    # last argument is teh instance
    if (
        args.dependencies
        and isinstance(
            args.dependencies[-1],
            SyntaxStepObjectInstantiation,
        )
        and lookup_class(
            args,
            args.dependencies[-1].object_type,
        )
    ):
        method_var_decl_type = args.dependencies[-1].object_type

    if dcl := lookup_var_state_by_name(args, method_var):
        if isinstance(dcl.meta.value, dict):
            analyze_method_invocation_values_dict(args, dcl, method_path)
        if isinstance(dcl.meta.value, str):
            analyze_method_invocation_values_str(args, dcl, method_path)
        if isinstance(dcl.meta.value, list):
            analyze_method_invocation_values_list(args, dcl, method_path)
    elif _method := lookup_method(args, method) or (
        _method := lookup_method(
            args,
            method_path or method_var,  # can be local function
            method_var_decl_type,
        )
    ):
        class_instance = (
            JavaClassInstance(
                fields={},
                class_name=method_var_decl_type,
            )
            if lookup_class(args, _method.metadata.class_name)
            else None
        )

        if return_step := args.eval_method(
            args,
            _method.metadata.n_id,
            args.dependencies,
            args.graph_db.shards_by_path_f(_method.shard_path),
            class_instance,
        ):
            args.syntax_step.meta.danger = return_step.meta.danger
            args.syntax_step.meta.value = return_step.meta.value
        if class_instance and args.syntax_step.current_instance:
            args.syntax_step.current_instance.fields.update(
                class_instance.fields
            )


def analyze_method_invocation_values_dict(
    args: EvaluatorArgs,
    dcl: SyntaxStep,
    method_path: str,
) -> None:
    if method_path == "put":
        value, key = args.dependencies
        dcl.meta.value[key.meta.value] = value
    elif method_path == "get":
        key = args.dependencies[0]
        args.syntax_step.meta.value = dcl.meta.value.get(key.meta.value)
        args.syntax_step.meta.danger = (
            dcl.meta.value[key.meta.value].meta.danger
            if key.meta.value in dcl.meta.value
            else False
        )


def analyze_method_invocation_values_str(
    args: EvaluatorArgs,
    dcl: SyntaxStep,
    method_path: str,
) -> None:
    if method_path == "charAt":
        index = int(args.dependencies[0].meta.value)
        args.syntax_step.meta.value = dcl.meta.value[index]


def analyze_method_invocation_values_list(
    args: EvaluatorArgs,
    dcl: SyntaxStep,
    method_path: str,
) -> None:
    methods = {
        "add": java_list_add,
        "remove": java_list_remove,
        "get": javascript_list_get,
        "pop": javascript_list_pop,
        "shift": javascript_list_shift,
        "push": javascript_list_push,
        "concat": javascript_list_concat,
    }
    if method := methods.get(method_path):
        method(args, dcl)
