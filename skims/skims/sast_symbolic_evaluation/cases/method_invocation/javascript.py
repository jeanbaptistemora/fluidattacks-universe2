import functools
from model.graph_model import (
    GraphShardMetadataLanguage,
    SyntaxStepDeclaration,
    SyntaxStepLambdaExpression,
    SyntaxStepLiteral,
    SyntaxStepMethodInvocation,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)
from sast_symbolic_evaluation.utils_generic import (
    complete_attrs_on_dict,
    lookup_var_dcl_by_name,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from typing import (
    Callable,
    Dict,
    Optional,
    Set,
)
from utils.string import (
    split_on_first_dot,
)

TFun = Callable[[EvaluatorArgs], None]
RETURNS = {
    "child_process": "child_process",
    "express": "core.Express",
}
TYPES: Dict[str, Set[str]] = complete_attrs_on_dict(
    {
        "core.Express.Router": {"get", "post", "put", "delete"},
    }
)


def javascript_only(
    func: TFun,
) -> Callable[[EvaluatorArgs], Optional[TFun]]:
    @functools.wraps(func)
    def wrapper_decorator(args: EvaluatorArgs) -> Optional[TFun]:
        if (
            args.shard.metadata.language
            != GraphShardMetadataLanguage.JAVASCRIPT
        ):
            return None
        return func(args)

    return wrapper_decorator


def evaluate_required(args: EvaluatorArgs) -> None:
    returns = {
        "child_process": "child_process",
        "express": "core.Express",
        "fs": "fs",
        "path": "PlatformPath",
    }
    method: SyntaxStepMethodInvocation = args.syntax_step
    if method.method != "require":
        return

    module: SyntaxStepLiteral = args.dependencies[0]
    if isinstance(module, SyntaxStepLiteral):
        method.return_type = returns.get(module.value)


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
        elif declaration.return_type and isinstance(
            declaration, SyntaxStepMethodInvocation
        ):
            args.syntax_step.var_type = declaration.return_type
        elif (
            method_var
            and not declaration.return_type
            and (method_var_decl := lookup_var_dcl_by_name(args, method_var))
        ):
            step.var_type = f"{method_var_decl.var_type}.{method_path}"


def _proccess_express_handler(
    args: EvaluatorArgs, handler: SyntaxStepLambdaExpression
) -> None:
    # the arguments are marked here because lambda functions are preprocessed,
    # so the arguments cannot be marked in the evaluator of the lambda function
    index = None
    handler.lambda_type = "RequestHandler"
    for index, step in enumerate(reversed(args.syntax_steps)):
        if step.meta.n_id == handler.meta.n_id:
            index = len(args.syntax_steps) - (index + 1)
            break
    else:
        return

    handler_arguments = get_dependencies(
        index,
        args.syntax_steps,
    )
    req: SyntaxStepDeclaration
    res: SyntaxStepDeclaration

    if len(handler_arguments) == 1:
        # pylint: disable=unbalanced-tuple-unpacking
        (req,) = handler_arguments
    elif len(handler_arguments) == 2:
        # pylint: disable=unbalanced-tuple-unpacking
        req, res = handler_arguments
    elif len(handler_arguments) == 3:
        # pylint: disable=unbalanced-tuple-unpacking
        req, res, _ = handler_arguments

    # add the type to the parameters, the type is only known
    # at runtime
    req.var_type = "Request"
    res.var_type = "Response"


@javascript_only
def process_express_requests(args: EvaluatorArgs) -> None:
    method_var, method_path = split_on_first_dot(args.syntax_step.method)
    if (
        method_var
        and (method_var_decl := lookup_var_dcl_by_name(args, method_var))
        # pylint: disable=used-before-assignment
        and (var_type := method_var_decl.var_type)
        and method_path in TYPES.get(var_type, set())
    ):
        handlers = [
            dep
            for dep in args.dependencies
            if isinstance(dep, SyntaxStepLambdaExpression)
        ]
        for handler in handlers:
            _proccess_express_handler(args, handler)


def process(args: EvaluatorArgs) -> None:
    evaluate_required(args)
    process_express_requests(args)
