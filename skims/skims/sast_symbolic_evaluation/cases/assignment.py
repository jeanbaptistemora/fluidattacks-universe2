from contextlib import (
    suppress,
)
from model.graph_model import (
    SyntaxStepMemberAccessExpression,
    SyntaxStepMeta,
)
from sast_symbolic_evaluation.decorators import (
    go_only,
    javascript_only,
)
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
    split_on_first_dot,
    split_on_last_dot,
)

# var type and vulnerable assignment
vuln_assign: Dict[str, Set[str]] = {
    "DirectoryEntry": {"AuthenticationTypes.None"},
}

# assignment of fields that make the object vulnerable
vuln_field_access: Dict[str, Set[str]] = complete_attrs_on_dict(
    {
        "System.Data.SqlClient.SqlCommand": {
            "CommandText",
        },
        "MySql.Data.MySqlClient.MySqlCommand": {
            "CommandText",
        },
        "System.Data.OracleClient.OracleCommand": {
            "CommandText",
        },
        "System.Data.SQLite.SQLiteCommand": {
            "CommandText",
        },
        "Npgsql.NpgsqlCommand": {
            "CommandText",
        },
        "System.DirectoryServices.DirectorySearcher": {
            "Filter",
        },
        "System.Web.HttpResponse": {
            "StatusDescription",
        },
        "System.Diagnostics.ProcessStartInfo": {
            "FileName",
        },
        "System.Diagnostics.Process": {
            "StartInfo",
        },
    }
)


@go_only
def go_evaluate_assignment(args: EvaluatorArgs) -> None:
    if len(args.dependencies) == 1 and (dep := args.dependencies[0]):
        # If the variable is a structure
        if (
            var_decl := lookup_var_dcl_by_name(args, args.syntax_step.var)
        ) and args.syntax_step.attribute:
            if var_decl.meta.value:
                var_decl.meta.value.update(
                    {
                        args.syntax_step.attribute: SyntaxStepMeta(
                            danger=dep.meta.danger,
                            dependencies=[],
                            n_id=dep.meta.n_id,
                            value=dep.meta.value,
                        )
                    }
                )
            else:
                var_decl.meta.value = {
                    args.syntax_step.attribute: SyntaxStepMeta(
                        danger=dep.meta.danger,
                        dependencies=[],
                        n_id=dep.meta.n_id,
                        value=dep.meta.value,
                    )
                }
            args.syntax_step.meta.value = var_decl.meta.value
            args.syntax_step.meta.danger = var_decl.meta.danger
        # Normal variables
        else:
            args.syntax_step.meta.value = args.dependencies[0].meta.value


@javascript_only
def javscript_evaluate_assignment(args: EvaluatorArgs) -> None:
    var, field = split_on_last_dot(args.syntax_step.var)
    var_decl = lookup_var_dcl_by_name(args, var)
    if (
        var_decl
        and var_decl.meta.value
        and isinstance(var_decl.meta.value, dict)
    ):
        var_decl.meta.value[field] = args.dependencies[-1]
    elif (
        var_decl
        and var_decl.meta.value
        and isinstance(var_decl.meta.value, list)
    ):
        with suppress(ValueError):
            index = int(field)
            if len(var_decl.meta.value) < index + 1:
                while len(var_decl.meta.value) < index + 1:
                    var_decl.meta.value.append(None)
            var_decl.meta.value[index] = args.dependencies[-1]


def evaluate(args: EvaluatorArgs) -> None:
    go_evaluate_assignment(args)
    javscript_evaluate_assignment(args)

    var, field = split_on_first_dot(args.syntax_step.var)
    [dependency] = args.dependencies

    if not args.syntax_step.meta.danger:
        args.syntax_step.meta.danger = dependency.meta.danger

    # modify the value of a field in an instance

    if args.current_instance:
        if var == "this":
            args.current_instance.fields[field] = args.syntax_step
        elif not field and lookup_field(args, var):
            args.current_instance.fields[var] = args.syntax_step

    elif v_dcl := lookup_var_dcl_by_name(args, var):
        if isinstance(v_dcl.meta.value, JavaClassInstance):
            v_dcl.meta.value.fields[field] = args.syntax_step

        if isinstance(
            dependency, SyntaxStepMemberAccessExpression
        ) and dependency.expression in vuln_assign.get(v_dcl.var_type, set()):
            args.syntax_step.meta.danger = True

        if field in vuln_field_access.get(v_dcl.var_type, set()):
            v_dcl.meta.danger = args.syntax_step.meta.danger
