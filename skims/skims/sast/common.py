# Standard library
from typing import (
    Any,
    Dict,
    Set,
    Tuple,
)

# Local library
from model import core_model


def build_attr_paths(*attrs: str) -> Set[str]:
    return set('.'.join(attrs[index:]) for index, _ in enumerate(attrs))


def split_on_first_dot(string: str) -> Tuple[str, str]:
    portions = string.split('.', maxsplit=1)
    if len(portions) == 2:
        return portions[0], portions[1]
    return portions[0], ''


def _complete_attrs_on_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        attr: value
        for path, value in data.items()
        for attr in build_attr_paths(*path.split('.'))
    }


def _complete_attrs_on_set(data: Set[str]) -> Set[str]:
    return {
        attr
        for path in data
        for attr in build_attr_paths(*path.split('.'))
    }


# Constants
DANGER_METHODS_BY_ARGS_PROPAGATION: Set[str] = _complete_attrs_on_set({
    'java.net.URLDecoder.decode',
    'java.nio.file.Files.newInputStream',
    'java.nio.file.Paths.get',
    'org.apache.commons.codec.binary.Base64.decodeBase64',
    'org.apache.commons.codec.binary.Base64.encodeBase64',
    'org.owasp.esapi.ESAPI.encoder.encodeForBase64',
    'org.owasp.esapi.ESAPI.encoder.decodeForBase64',
    'Double.toString',
    'Float.toString',
    'Integer.toString',
    'Long.toString',
})
DANGER_METHODS_STATIC_FINDING: Dict[str, Set[str]] = {
    core_model.FindingEnum.F034.name:
    _complete_attrs_on_set({
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
    core_model.FindingEnum.F034.name:
    _complete_attrs_on_set({
        'java.util.Random.nextBytes',
    }),
}
DANGER_METHODS_BY_OBJ_NO_TYPE_ARGS_PROPAGATION_FIDING: Dict[str, Set[str]] = {
    core_model.FindingEnum.F034.name:
    _complete_attrs_on_set({
        'getSession.setAttribute',
        'toString.substring',
        'addCookie',
    })
}
DANGER_METHODS_BY_OBJ: Dict[str, Set[str]] = _complete_attrs_on_dict({
    'java.lang.String': {
        'getBytes',
        'substring',
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
        'executeUpdate',
    },
    'org.owasp.benchmark.helpers.ThingInterface': {
        'doSomething',
    },
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
    core_model.FindingEnum.F042.name:
    _complete_attrs_on_dict({
        'javax.servlet.http.Cookie': {
            'setSecure': {
                False,
            },
        },
    })
}
DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION: Dict[
    str, Set[str]] = _complete_attrs_on_dict({
        'java.util.List': {
            'add',
        },
    })
DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION_FINDING: Dict[str, Dict[
    str, Set[str]]] = {
        core_model.FindingEnum.F042.name: _complete_attrs_on_dict({
            'javax.servlet.http.HttpServletResponse': {
                'addCookie',
            },
        }),
        core_model.FindingEnum.F034.name: _complete_attrs_on_dict({
            'javax.servlet.http.HttpServletResponse': {
                'addCookie',
            },
        }),
        core_model.FindingEnum.F004.name:
        _complete_attrs_on_dict({
            'ProcessBuilder': {
                'command',
            },
            'Runtime': {
                'exec',
            },
        }),
}
