# Standard library
from typing import (
    Tuple,
)

# Local libraries
from eval_java.model import (
    Statements,
)
from eval_java.eval_rules import (
    common,
)

# Constants
DANGER_METHODS_BY_ARGS_PROPAGATION = {
    'java.net.URLDecoder.decode',
}
DANGER_METHODS_BY_TYPE = {
    'HttpServletRequest': {
        'getCookies',
        'getHeader',
        'getHeaderNames',
        'getHeaders',
        'getParameter',
        'getParameterMap',
        'getParameterNames',
        'getParameterValues',
        'getQueryString',
    },
    'HttpServletResponse': {
        'getWriter',
    },
    'javax.servlet.http.Cookie': {
        'getName',
        'getValue',
    },
}


def _split_var_from_method(method: str) -> Tuple[str, str]:
    tokens = method.split('.', maxsplit=1)
    if len(tokens) == 2:
        return tokens[0], tokens[1]

    return tokens[0], ''


def evaluate(statements: Statements, index: int) -> None:
    statement = statements[index]

    # Analyze if the arguments involved in the function are dangerous
    args = common.read_stack(statements, index)
    args_danger = any(arg.meta.danger for arg in args)

    # Analyze if the call itself is sensitive
    method = statement.method
    method_var, method_path = _split_var_from_method(method)
    method_var_type = common.read_stack_var_type(
        statements, index, method_var,
    )

    # Local context
    statement.meta.danger = any((
        # Known function to return user controlled data
        method_path in DANGER_METHODS_BY_TYPE.get(method_var_type, {}),
        # Known functions that propagate args danger
        method in DANGER_METHODS_BY_ARGS_PROPAGATION and args_danger,
        # Insecure methods
        method in {
            'java.lang.Math.random',
            'lang.Math.random',
            'Math.random',
            'random',
        },
    ))
