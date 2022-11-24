from model.graph_model import (
    SyntaxStep,
    SyntaxStepDeclaration,
    SyntaxStepLiteral,
    SyntaxStepMethodInvocation,
    SyntaxStepObjectInstantiation,
    SyntaxStepSymbolLookup,
)
from sast_symbolic_evaluation.decorators import (
    javascript_only,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)
from sast_symbolic_evaluation.utils_generic import (
    complete_attrs_on_dict,
    lookup_var_dcl_by_name,
)
from typing import (
    Dict,
    Set,
    Union,
)
from utils.string import (
    split_on_first_dot,
)

TYPES: Dict[str, Set[str]] = complete_attrs_on_dict(
    {
        "express.Router": {"get", "post", "put", "delete"},
    }
)


def evaluate_required(args: EvaluatorArgs) -> None:
    method: SyntaxStepMethodInvocation = args.syntax_step
    if method.method != "require":
        return

    module: SyntaxStepLiteral = args.dependencies[0]
    if isinstance(module, SyntaxStepLiteral):
        method.return_type = str(module.value)


@javascript_only
def process_declaration(args: EvaluatorArgs) -> None:
    # javascript is a dynamic language the type of some
    # declarations is known at runtime
    step: SyntaxStepDeclaration = args.syntax_step
    if len(args.dependencies) == 1:
        (declaration,) = args.dependencies
        if not isinstance(declaration, SyntaxStepMethodInvocation):
            return
        method_var, method_path = split_on_first_dot(declaration.method)

        if declaration.return_type and args.syntax_step.is_destructuring:
            args.syntax_step.var_type = f"{declaration.return_type}.{step.var}"
        elif (
            method_var
            and not declaration.return_type
            and (method_var_decl := lookup_var_dcl_by_name(args, method_var))
            and isinstance(method_var_decl, SyntaxStepDeclaration)
        ):
            step.var_type = f"{method_var_decl.var_type}.{method_path}"


def process(args: EvaluatorArgs) -> None:
    evaluate_required(args)


def list_remove(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    index = int(args.dependencies[0].meta.value)
    dcl.meta.value.pop(index)
    dcl.meta.danger = any(x.meta.danger for x in dcl.meta.value if x)


def list_get(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    index = int(args.dependencies[0].meta.value)
    args.syntax_step.meta.value = dcl.meta.value[index]
    args.syntax_step.meta.danger = dcl.meta.value[index].meta.danger


def list_pop(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    last = dcl.meta.value.pop()
    args.syntax_step.meta.value = last.meta.value
    args.syntax_step.meta.danger = last.meta.danger
    dcl.meta.danger = any(x.meta.danger for x in dcl.meta.value if x)


def list_shift(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    firsts = dcl.meta.value.pop(0)
    args.syntax_step.meta.value = firsts.meta.value
    args.syntax_step.meta.danger = firsts.meta.danger
    dcl.meta.danger = any(x.meta.danger for x in dcl.meta.value if x)


def list_push(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    for argument in args.dependencies:
        dcl.meta.value.append(argument)
    args.syntax_step.meta.value = len(dcl.meta.value)
    dcl.meta.danger = any(x.meta.danger for x in dcl.meta.value if x)


def list_concat(args: EvaluatorArgs, dcl: SyntaxStep) -> None:
    new_list = dcl.meta.value
    for argument in args.dependencies:
        if argument.meta.value and isinstance(argument.meta.value, list):
            new_list.extend(argument.meta.value)
    args.syntax_step.meta.value = new_list
    args.syntax_step.meta.danger = any(
        x.meta.danger for x in args.syntax_step.meta.value if x
    )


@javascript_only
def process_cookie(args: EvaluatorArgs) -> None:
    for _arg in args.dependencies:
        _arg_value = _arg.meta.value
        if not isinstance(_arg_value, dict):
            continue
        if _secure := _arg_value.get("secure"):
            args.syntax_step.meta.danger = _secure.meta.value is False


def insecure_mysql_query(args: EvaluatorArgs) -> None:
    arguments = args.dependencies
    query: Union[
        SyntaxStepObjectInstantiation,
        SyntaxStepLiteral,
        SyntaxStepSymbolLookup,
    ] = arguments[-1]
    if (
        isinstance(query, SyntaxStepObjectInstantiation)
        and query.meta.value
        and (sql := query.meta.value.get("sql"))
    ):
        args.syntax_step.meta.danger = sql.meta.danger
    else:
        args.syntax_step.meta.danger = query.meta.danger
