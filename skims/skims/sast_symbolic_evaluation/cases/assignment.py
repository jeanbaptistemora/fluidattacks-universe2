from contextlib import (
    suppress,
)
from model.graph_model import (
    GraphShardMetadataLanguage,
    SyntaxStepMeta,
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
    split_on_last_dot,
)

# assignment of fields that make the object vulnerable
BY_TYPE: Dict[str, Set[str]] = complete_attrs_on_dict(
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


def go_evaluate_assignment(args: EvaluatorArgs) -> None:
    if (
        args.shard.metadata.language == GraphShardMetadataLanguage.GO
        and len(args.dependencies) == 1
        and (dep := args.dependencies[0])
    ):
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


def javscript_evaluate_assignment(args: EvaluatorArgs) -> bool:
    var, field = split_on_last_dot(args.syntax_step.var)
    var_decl = lookup_var_dcl_by_name(args, var)
    if (
        var_decl
        and var_decl.meta.value
        and isinstance(var_decl.meta.value, dict)
    ):
        var_decl.meta.value[field] = args.dependencies[-1]
        return True
    if (
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
        return True

    return False


def evaluate(args: EvaluatorArgs) -> None:
    danger_assignment = {
        "AuthenticationTypes.None",
    }
    vulnerable_type = {
        "DirectoryEntry",
    }
    var, field = split_on_last_dot(args.syntax_step.var)
    args_danger = any(dep.meta.danger for dep in args.dependencies)
    if not args.syntax_step.meta.danger:
        args.syntax_step.meta.danger = args_danger

    go_evaluate_assignment(args)
    javscript_evaluate_assignment(args)
    # modify the value of a field in an instance
    if var != "this":
        var_decl = lookup_var_dcl_by_name(args, var)
        # pylint:disable=used-before-assignment
        if (
            var_decl
            and var_decl.var_type in vulnerable_type
            and args.dependencies.pop().expression in danger_assignment
        ):
            args.syntax_step.meta.danger = True
        if var_decl and isinstance(
            var_decl.meta.value,
            JavaClassInstance,
        ):
            var_decl.meta.value.fields[field] = args.syntax_step
        elif args.current_instance and not field and lookup_field(args, var):
            args.current_instance.fields[var] = args.syntax_step
        elif var_decl and field in BY_TYPE.get(var_decl.var_type, set()):
            var_decl.meta.danger = args.syntax_step.meta.danger
    elif args.current_instance and var == "this":
        _, field = split_on_last_dot(args.syntax_step.var)
        args.current_instance.fields[field] = args.syntax_step
