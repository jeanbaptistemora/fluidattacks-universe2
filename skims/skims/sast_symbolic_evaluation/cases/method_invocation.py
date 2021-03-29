# Local libraries
from typing import (
    Any,
    Dict,
    Set,
)
from model import (
    graph_model,
)
from model import (
    core_model,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
)
from sast_symbolic_evaluation.utils_generic import (
    lookup_var_dcl_by_name,
    lookup_var_state_by_name,
)
from sast_symbolic_evaluation.utils_java import (
    lookup_java_field,
    lookup_java_method,
)
from utils.string import (
    build_attr_paths,
    complete_attrs_on_set,
    split_on_first_dot,
    split_on_last_dot,
)


def _complete_attrs_on_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        attr: value
        for path, value in data.items()
        for attr in build_attr_paths(*path.split('.'))
    }


DANGER_METHODS_BY_ARGS_PROPAGATION: Set[str] = complete_attrs_on_set({
    'java.net.URLDecoder.decode',
    'java.nio.file.Files.newInputStream',
    'java.nio.file.Paths.get',
    'org.apache.commons.codec.binary.Base64.decodeBase64',
    'org.apache.commons.codec.binary.Base64.encodeBase64',
    'org.springframework.jdbc.core.JdbcTemplate.batchUpdate',
    'org.springframework.jdbc.core.JdbcTemplate.execute',
    'org.springframework.jdbc.core.JdbcTemplate.query',
    'org.springframework.jdbc.core.JdbcTemplate.queryForInt',
    'org.springframework.jdbc.core.JdbcTemplate.queryForList',
    'org.springframework.jdbc.core.JdbcTemplate.queryForLong',
    'org.springframework.jdbc.core.JdbcTemplate.queryForMap',
    'org.springframework.jdbc.core.JdbcTemplate.queryForObject',
    'org.springframework.jdbc.core.JdbcTemplate.queryForRowSet',
    'org.owasp.esapi.ESAPI.encoder.encodeForBase64',
    'org.owasp.esapi.ESAPI.encoder.decodeForBase64',
    'Double.toString',
    'Float.toString',
    'Integer.toString',
    'Long.toString',
})
DANGER_METHODS_STATIC_FINDING: Dict[str, Set[str]] = {
    core_model.FindingEnum.F034.name: complete_attrs_on_set({
        'java.lang.Math.random',
        'java.util.Random.nextFloat',
        'java.util.Random.nextInt',
        'java.util.Random.nextLong',
        'java.util.Random.nextBoolean',
        'java.util.Random.nextDouble',
        'java.util.Random.nextGaussian',
    }),
}
DANGER_METHODS_STATIC_SIDE_EFFECTS_FINDING: Dict[str, Set[str]] = {
    core_model.FindingEnum.F034.name: complete_attrs_on_set({
        'java.util.Random.nextBytes',
    }),
}
DANGER_METHODS_BY_OBJ_NO_TYPE_ARGS_PROPAGATION_FIDING: Dict[str, Set[str]] = {
    core_model.FindingEnum.F034.name: complete_attrs_on_set({
        'getSession.setAttribute',
        'toString.substring',
        'addCookie',
    }),
    core_model.FindingEnum.F063_TRUSTBOUND.name: complete_attrs_on_set({
        'org.apache.commons.lang.StringEscapeUtils.escapeHtml',
        'org.springframework.web.util.HtmlUtils.htmlEscape',
        'org.owasp.esapi.ESAPI.encoder.encodeForHTML',
    }),
}
DANGER_METHODS_BY_OBJ: Dict[str, Set[str]] = _complete_attrs_on_dict({
    'java.lang.String': {
        'getBytes',
        'split',
        'substring',
        'toCharArray',
    },
    'java.lang.StringBuilder': {
        'append',
        'append.toString',
        'toString',
    },
    'java.sql.CallableStatement': {
        'executeQuery',
    },
    'java.sql.PreparedStatement': {
        'execute',
    },
    'java.util.Enumeration': {
        'nextElement',
    },
    'java.util.Map': {
        'get',
    },
    'java.util.List': {
        'get',
    },
    'org.owasp.benchmark.helpers.SeparateClassRequest': {
        'getTheParameter',
    },
})
DANGER_METHODS_BY_OBJ_ARGS: Dict[str, Set[str]] = _complete_attrs_on_dict({
    'java.sql.Connection': {
        'prepareCall',
        'prepareStatement',
    },
    'java.sql.Statement': {
        'addBatch',
        'execute',
        'executeBatch',
        'executeLargeBatch',
        'executeLargeUpdate',
        'executeQuery',
        'executeUpdate',
    },
    'org.owasp.benchmark.helpers.ThingInterface': {
        'doSomething',
    },
    'javax.xml.xpath.XPath': {
        'evaluate',
        'compile',
    }
})
DANGER_METHODS_BY_TYPE: Dict[str, Set[str]] = _complete_attrs_on_dict({
    'javax.servlet.http.Cookie': {
        'getName',
        'getValue',
    },
    'javax.servlet.http.HttpServletRequest': {
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
})
DANGER_METHODS_BY_TYPE_AND_VALUE_FINDING: Dict[str, Dict[str, Any]] = {
    core_model.FindingEnum.F008.name: _complete_attrs_on_dict({
        'javax.servlet.http.HttpServletResponse': {
            'setHeader': {
                'X-XSS-Protection',
                '0',
            },
        },
    }),
    core_model.FindingEnum.F042.name: _complete_attrs_on_dict({
        'javax.servlet.http.Cookie': {
            'setSecure': {
                False,
            },
        },
    }),
}
DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION: Dict[str, Set[str]] = \
    _complete_attrs_on_dict({
        'java.io.PrintWriter': {
            'format',
        },
        'java.util.List': {
            'add',
        },
    })
DANGER_METHODS_BY_TYPE_ARGS_PROPAG_FINDING: Dict[str, Dict[str, Set[str]]] = {
    core_model.FindingEnum.F042.name: _complete_attrs_on_dict({
        'javax.servlet.http.HttpServletResponse': {
            'addCookie',
        },
    }),
    core_model.FindingEnum.F034.name: _complete_attrs_on_dict({
        'javax.servlet.http.HttpServletResponse': {
            'addCookie',
        },
        'javax.servlet.http.HttpServletRequest': {
            'getSession.setAttribute',
        },
    }),
    core_model.FindingEnum.F004.name: _complete_attrs_on_dict({
        'ProcessBuilder': {
            'command',
        },
        'Runtime': {
            'exec',
        },
    }),
    core_model.FindingEnum.F008.name: _complete_attrs_on_dict({
        'javax.servlet.http.HttpServletResponse': {
            'getWriter.format',
            'getWriter.print',
            'getWriter.printf',
            'getWriter.println',
            'getWriter.write',
        },
    }),
    core_model.FindingEnum.F063_TRUSTBOUND.name: _complete_attrs_on_dict({
        'javax.servlet.http.HttpServletRequest': {
            'getSession.putValue',
            'getSession.setAttribute',
        },
    }),
    core_model.FindingEnum.F107.name: _complete_attrs_on_dict({
        'javax.naming.directory.InitialDirContext': {
            'search',
        },
        'javax.naming.directory.DirContext': {
            'search',
        },
    }),
}


def evaluate(args: EvaluatorArgs) -> None:
    # Analyze if the method itself is untrusted
    method = args.syntax_step.method

    analyze_method_invocation(args, method)
    analyze_method_invocation_values(args)


def analyze_method_invocation(args: EvaluatorArgs, method: str) -> None:
    # Analyze the arguments involved in the method invocation
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    method_var, method_path = split_on_first_dot(method)
    method_field, method_name = split_on_last_dot(args.syntax_step.method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)
    method_var_state = lookup_var_state_by_name(args, method_var)
    method_var_decl_type = (
        method_var_decl.var_type_base if method_var_decl else ''
    )

    if field := lookup_java_field(args, method_field):
        method = f'{field.var_type}.{method_name}'

    args.syntax_step.meta.danger = (
        # Known function to return user controlled data
        method_path in DANGER_METHODS_BY_TYPE.get(method_var_decl_type, {})
    ) or (
        # Know functions that propagate danger if object is dangerous
        method_path in DANGER_METHODS_BY_OBJ.get(method_var_decl_type, {})
        and method_var_state
        and method_var_state.meta.danger
    ) or (
        # Know functions that propagate danger if args are dangerous
        method_path in DANGER_METHODS_BY_OBJ_ARGS.get(method_var_decl_type, {})
        and args_danger
    ) or (
        # Known functions that propagate args danger
        method in DANGER_METHODS_BY_ARGS_PROPAGATION
        and args_danger
    ) or (
        # Known static functions that no require args danger
        method in DANGER_METHODS_STATIC_FINDING.get(
            args.finding.name,
            set(),
        )
    ) or (
        # functions for which the type of the variable cannot be obtained,
        # but which propagate args danger
        method_path
        and method_path in
        DANGER_METHODS_BY_OBJ_NO_TYPE_ARGS_PROPAGATION_FIDING.get(
            args.finding.name, str())
        and args_danger
    )
    analyze_method_static_side_effects(args, method)
    analyze_method_by_type_args_propagation(args, method)
    analyze_method_by_type_args_propagation_side_effects(args, method)

    # function calls with parameters that make the object vulnerable
    if methods := DANGER_METHODS_BY_TYPE_AND_VALUE_FINDING.get(
            args.finding.name,
            dict(),
    ).get(method_var_decl_type):
        parameters = {param.meta.value for param in args.dependencies}
        if (
            parameters.issubset(methods.get(method_path, set()))
            and method_var_decl
        ):
            method_var_decl.meta.danger = True


def analyze_method_invocation_values(args: EvaluatorArgs) -> None:
    method_var, method_path = split_on_first_dot(args.syntax_step.method)

    if dcl := lookup_var_state_by_name(args, method_var):
        if isinstance(dcl.meta.value, dict):
            analyze_method_invocation_values_dict(args, dcl, method_path)
        if isinstance(dcl.meta.value, str):
            analyze_method_invocation_values_str(args, dcl, method_path)
        if isinstance(dcl.meta.value, list):
            analyze_method_invocation_values_list(args, dcl, method_path)
    elif method := lookup_java_method(args, args.syntax_step.method):
        if return_step := args.eval_method(
            args, method.n_id, args.dependencies,
        ):
            args.syntax_step.meta.danger = return_step.meta.danger
            args.syntax_step.meta.value = return_step.meta.value


def analyze_method_invocation_values_dict(
    args: EvaluatorArgs,
    dcl: graph_model.SyntaxStep,
    method_path: str,
) -> None:
    if method_path == 'put':
        value, key = args.dependencies
        dcl.meta.value[key.meta.value] = value
    elif method_path == 'get':
        key = args.dependencies[0]
        args.syntax_step.meta.value = dcl.meta.value.get(key.meta.value)
        args.syntax_step.meta.danger = (
            dcl.meta.value[key.meta.value].meta.danger
            if key.meta.value in dcl.meta.value
            else False
        )


def analyze_method_invocation_values_str(
    args: EvaluatorArgs,
    dcl: graph_model.SyntaxStep,
    method_path: str,
) -> None:
    if method_path == 'charAt':
        index = int(args.dependencies[0].meta.value)
        args.syntax_step.meta.value = dcl.meta.value[index]


def analyze_method_invocation_values_list(
    args: EvaluatorArgs,
    dcl: graph_model.SyntaxStep,
    method_path: str,
) -> None:
    if method_path == 'add':
        dcl.meta.value.append(args.dependencies[0])
    elif method_path == 'remove':
        index = int(args.dependencies[0].meta.value)
        dcl.meta.value.pop(index)
    elif method_path == 'get':
        index = int(args.dependencies[0].meta.value)
        args.syntax_step.meta.value = dcl.meta.value[index]
        args.syntax_step.meta.danger = dcl.meta.value[index].meta.danger


def analyze_method_static_side_effects(
    args: EvaluatorArgs,
    method: str,
) -> None:
    # functions that make its parameters vulnerable
    if method in DANGER_METHODS_STATIC_SIDE_EFFECTS_FINDING.get(
            args.finding.name, set()):
        for dep in args.dependencies:
            dep.meta.danger = True


def analyze_method_by_type_args_propagation_side_effects(
    args: EvaluatorArgs,
    method: str,
) -> None:
    # Functions that when called make the parent object vulnerable
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    method_var, method_path = split_on_first_dot(method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)
    method_var_decl_type = (method_var_decl.var_type_base
                            if method_var_decl else '')

    if (method_path in DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION.get(
            method_var_decl_type, {}) and args_danger):
        if method_var_decl:
            method_var_decl.meta.danger = True


def analyze_method_by_type_args_propagation(
    args: EvaluatorArgs,
    method: str,
) -> None:
    # Functions that when called make the parent object vulnerable
    args_danger = any(dep.meta.danger for dep in args.dependencies)

    method_var, method_path = split_on_first_dot(method)
    method_var_decl = lookup_var_dcl_by_name(args, method_var)
    method_var_decl_type = (method_var_decl.var_type_base
                            if method_var_decl else '')

    if (method_path in DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION.get(
            method_var_decl_type, {}) and args_danger):
        args.syntax_step.meta.danger = True

    danger_methods = DANGER_METHODS_BY_TYPE_ARGS_PROPAG_FINDING.get(
        args.finding.name, {})
    if (method_path in danger_methods.get(
            method_var_decl_type, {}) and args_danger):
        args.syntax_step.meta.danger = True
