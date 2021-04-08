# Local libraries
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    JavaClassInstance,
)
from sast_symbolic_evaluation.utils_generic import (
    lookup_var_dcl_by_name,
)
from utils.string import (
    split_on_last_dot,
)


def evaluate(args: EvaluatorArgs) -> None:
    args_danger = any(dep.meta.danger for dep in args.dependencies)
    if not args.syntax_step.meta.danger:
        args.syntax_step.meta.danger = args_danger

    # modify the value of a field in an instance
    if '.' in args.syntax_step.var and not args.syntax_step.var.startswith(
            'this.'):
        var, field = split_on_last_dot(args.syntax_step.var)
        # pylint:disable=used-before-assignment
        if (var_decl := lookup_var_dcl_by_name(args, var)) and isinstance(
                var_decl.meta.value,
                JavaClassInstance,
        ):
            var_decl.meta.value.fields[field] = args.syntax_step.meta.value
