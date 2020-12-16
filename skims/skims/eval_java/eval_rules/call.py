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
    'java.nio.file.Files.newInputStream',
    'java.nio.file.Paths.get',
    'org.apache.commons.codec.binary.Base64.decodeBase64',
    'org.apache.commons.codec.binary.Base64.encodeBase64',
}
DANGER_METHODS_BY_OBJ = {
    'java.util.Enumeration': {
        'nextElement',
    },
    'java.util.Map': {
        'get',
    },
    'String': {
        'getBytes',
    },
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


def _split_diamond_from_var_type(method: str) -> Tuple[str, str]:
    tokens = method.rsplit('<', maxsplit=1)
    if len(tokens) == 2:
        return tokens[0], tokens[1][0:-1]

    return tokens[0], ''


def evaluate(statements: Statements, index: int) -> None:
    statement = statements[index]

    # Analyze if the arguments involved in the function are dangerous
    args = common.read_stack(statements, index)
    args_danger = any(arg.meta.danger for arg in args)

    # Analyze if the call itself is sensitive
    method = statement.method
    method_var, method_path = _split_var_from_method(method)
    method_var_stmt = common.read_stack_var(
        statements, index, method_var,
    )
    method_var_type, _ = _split_diamond_from_var_type(
        common.read_stack_var_type(
            statements, index, method_var,
        ),
    )

    # Local context
    statement.meta.danger = (
        # Known function to return user controlled data
        method_path in DANGER_METHODS_BY_TYPE.get(method_var_type, {})
    ) or (
        # Know functions that propagate danger if object is dangerous
        method_path in DANGER_METHODS_BY_OBJ.get(method_var_type, {})
        and method_var_stmt
        and method_var_stmt.meta.danger
    ) or (
        # Known functions that propagate args danger
        method in DANGER_METHODS_BY_ARGS_PROPAGATION
        and args_danger
    ) or (
        # Insecure methods
        method in {
            'java.lang.Math.random',
            'lang.Math.random',
            'Math.random',
            'random',
        }
    )
