from model.graph_model import (
    GraphShardMetadataLanguage,
    SyntaxStep,
    SyntaxStepDeclaration,
    SyntaxStepObjectInstantiation,
    SyntaxStepSymbolLookup,
)
from sast_symbolic_evaluation.cases.method_invocation.constants import (
    BY_OBJ_NO_TYPE_ARGS_PROPAG,
)
from sast_symbolic_evaluation.cases.method_invocation.go import (
    attempt_go_parse_float,
)
from sast_symbolic_evaluation.cases.method_invocation.java import (
    list_add as java_list_add,
    list_remove as java_list_remove,
)
from sast_symbolic_evaluation.cases.method_invocation.javascript import (
    list_concat as javascript_list_concat,
    list_get as javascript_list_get,
    list_pop as javascript_list_pop,
    list_push as javascript_list_push,
    list_shift as javascript_list_shift,
)
from sast_symbolic_evaluation.lookup import (
    lookup_class,
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
)


def evaluate(args: EvaluatorArgs) -> None:
    language = args.shard.metadata.language
    if language == GraphShardMetadataLanguage.GO:
        evaluate_go(args)


def evaluate_go(args: EvaluatorArgs) -> None:
    # pylint: disable=expression-not-assigned
    (attempt_go_parse_float(args) or attempt_the_old_way(args))


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


def attempt_the_old_way(args: EvaluatorArgs) -> bool:
    # Analyze if the method itself is untrusted
    method = args.syntax_step.method
    analyze_method_invocation(args, method)
    analyze_method_invocation_values(args)
    return False


def analyze_method_invocation(args: EvaluatorArgs, method: str) -> None:
    method_var, _ = split_on_first_dot(method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)
    # pylint: disable=expression-not-assigned
    (
        attempt_by_args_propagation_no_type(args, method)
        or analyze_method_invocation_local(args, method)
        or analyze_method_invocation_external(args, method, method_var_decl)
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

    if method_var_decl and isinstance(method_var_decl, SyntaxStepDeclaration):
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
        (
            _method := lookup_method(
                args,
                method_path,
                method_var_decl_type,
            )
        )
        and args.shard.path != _method.shard_path
        and (
            return_step := args.eval_method(
                args,
                _method.metadata.n_id,
                args.dependencies,
                args.graph_db.shards_by_path_f(_method.shard_path),
                method_var_decl.meta.value if method_var_decl else None,
            )
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
            if lookup_class(args, str(_method.metadata.class_name))
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
