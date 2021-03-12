# Standard library
from typing import (
    Dict,
    Set,
    Tuple,
)


def build_attr_paths(*attrs: str) -> Set[str]:
    return set('.'.join(attrs[index:]) for index, _ in enumerate(attrs))


def split_on_first_dot(string: str) -> Tuple[str, str]:
    portions = string.split('.', maxsplit=1)
    if len(portions) == 2:
        return portions[0], portions[1]
    return portions[0], ''


def _complete_attrs_on_dict(data: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
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
DANGER_METHODS_STATIC: Set[str] = _complete_attrs_on_set({
    'java.lang.Math.random',
    'java.util.Random.nextFloat',
    'java.util.Random.nextInt',
    'java.util.Random.nextLong',
    'java.util.Random.nextBoolean',
    'java.util.Random.nextDouble',
    'java.util.Random.nextGaussian',
})
DANGER_METHODS_STATIC_SIDE_EFFECTS = _complete_attrs_on_set({
    'java.util.Random.nextBytes',
})
DANGER_METHODS_BY_OBJ_NO_TYPE_ARGS_PROPAGATION: Set[
    str] = _complete_attrs_on_set({
        'getSession.setAttribute',
        'toString.substring',
        'addCookie',
    })
DANGER_METHODS_BY_OBJ: Dict[str, Set[str]] = _complete_attrs_on_dict({
    'java.lang.String': {
        'getBytes',
        'substring',
    },
    'java.util.Enumeration': {
        'nextElement',
    },
    'java.util.Map': {
        'get',
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
    'javax.servlet.http.HttpServletResponse': {
        'getWriter',
        'addCookie'
    },
})
DANGER_METHODS_BY_TYPE_ARGS_PROPAGATION: Dict[
    str, Set[str]] = _complete_attrs_on_dict({
        'java.util.List': {
            'add',
        },
        'ProcessBuilder': {
            'command',
        },
        'Runtime': {
            'exec',
        },
    })
