from sast_symbolic_evaluation.lookup import (
    lookup_field,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    JavaClassInstance,
)
from sast_symbolic_evaluation.utils_generic import (
    complete_attrs_on_dict,
    lookup_var_dcl_by_name,
)
from typing import (
    Dict,
    Set,
)
from utils.string import (
    split_on_last_dot,
)

# assignment of fields that make the object vulnerable
BY_TYPE: Dict[str, Set[str]] = complete_attrs_on_dict(
    {
        "System.Data.SqlClient.SqlCommand": {
            "CommandText",
        },
        "System.DirectoryServices.DirectorySearcher": {
            "Filter",
        },
    }
)


def evaluate(args: EvaluatorArgs) -> None:
    var, field = split_on_last_dot(args.syntax_step.var)
    args_danger = any(dep.meta.danger for dep in args.dependencies)
    if not args.syntax_step.meta.danger:
        args.syntax_step.meta.danger = args_danger

    # modify the value of a field in an instance
    if var != "this":
        # pylint:disable=used-before-assignment
        if (var_decl := lookup_var_dcl_by_name(args, var)) and isinstance(
            var_decl.meta.value,
            JavaClassInstance,
        ):
            var_decl.meta.value.fields[field] = args.syntax_step
        elif args.current_instance and not field and lookup_field(args, var):
            args.current_instance.fields[var] = args.syntax_step
        elif (
            var_decl := lookup_var_dcl_by_name(args, var)
        ) and field in BY_TYPE.get(var_decl.var_type, set()):
            var_decl.meta.danger = args.syntax_step.meta.danger
    elif args.current_instance and var == "this":
        _, field = split_on_last_dot(args.syntax_step.var)
        args.current_instance.fields[field] = args.syntax_step
