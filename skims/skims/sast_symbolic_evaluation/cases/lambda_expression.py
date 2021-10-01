from model.graph_model import (
    SyntaxStepMethodInvocation,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)
from sast_symbolic_evaluation.utils_generic import (
    complete_attrs_on_dict,
    lookup_var_dcl_by_name,
)
from utils.string import (
    split_on_last_dot,
)

PARAM_TYPES = complete_attrs_on_dict(
    {
        "mysql.PoolCluster": {
            "getConnection": ("mysql.MysqlError", "mysql.PoolConnection"),
        },
        "mysql.Pool": {
            "getConnection": ("mysql.MysqlError", "mysql.PoolConnection"),
        },
    }
)


def evaluate(args: EvaluatorArgs) -> None:
    las_statement: SyntaxStepMethodInvocation = args.syntax_steps[-1]
    if isinstance(las_statement, SyntaxStepMethodInvocation):
        var, method_path = split_on_last_dot(las_statement.method)
        # pylint: disable=used-before-assignment
        if (
            (var_decl := lookup_var_dcl_by_name(args, var))
            and (
                param_types := PARAM_TYPES.get(var_decl.var_type, {}).get(
                    method_path
                )
            )
            and len(param_types) == len(args.dependencies)
        ):
            for param_type, param in zip(param_types, args.dependencies):
                param.var_type = param_type
