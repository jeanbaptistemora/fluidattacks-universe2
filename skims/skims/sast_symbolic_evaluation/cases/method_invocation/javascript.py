from model.graph_model import (
    SyntaxStep,
    SyntaxStepDeclaration,
    SyntaxStepLambdaExpression,
    SyntaxStepLiteral,
    SyntaxStepMethodInvocation,
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
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from typing import (
    Dict,
    Set,
)
from utils.crypto import (
    insecure_elliptic_curve,
    is_vulnerable_cipher,
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
        method.return_type = module.value


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


@javascript_only
def insecure_key(args: EvaluatorArgs) -> None:
    arguments = args.dependencies
    if len(arguments) < 2:
        return None
    *_, _options, key_type = arguments
    options = _options.meta.value
    if (
        key_type.meta.value == "rsa"
        and isinstance(options, dict)
        and (key_length := options.get("modulusLength"))
    ):
        args.syntax_step.meta.danger = (
            key_length.meta.value and key_length.meta.value < 2048
        )
    elif (
        key_type.meta.value == "ec"
        and isinstance(options, dict)
        and (curve_name := options.get("namedCurve"))
    ):
        args.syntax_step.meta.danger = (
            curve_name.meta.value
            and insecure_elliptic_curve(curve_name.meta.value)
        )
    return None


@javascript_only
def insecure_crypto_js(args: EvaluatorArgs) -> None:
    arguments = args.dependencies
    if len(arguments) < 3:
        return None

    algorithm = ""
    if "aes" in args.syntax_step.method.lower():
        algorithm = "aes"
    elif "rsa" in args.syntax_step.method.lower():
        algorithm = "rsa"
    else:
        return None

    *_, _options, _, _ = arguments
    options = _options.meta.value
    cipher_mode = options.get("mode")
    cipher_padding = options.get("padding")

    args.syntax_step.meta.danger = is_vulnerable_cipher(
        algorithm,
        cipher_mode.member
        if cipher_padding.type == "SyntaxStepMemberAccessExpression"
        else None,
        cipher_padding.member
        if cipher_padding
        and cipher_padding.type == "SyntaxStepMemberAccessExpression"
        else None,
    )

    return None
