# Standard library
from typing import (
    Dict,
    Set,
)


def build_attr_paths(*attrs: str) -> Set[str]:
    return set('.'.join(attrs[index:]) for index, _ in enumerate(attrs))


# Constants
DANGER_METHODS_BY_ARGS_PROPAGATION: Set[str] = {
    'java.net.URLDecoder.decode',
    'java.nio.file.Files.newInputStream',
    'java.nio.file.Paths.get',
    'org.apache.commons.codec.binary.Base64.decodeBase64',
    'org.apache.commons.codec.binary.Base64.encodeBase64',
}
DANGER_METHODS_BY_OBJ: Dict[str, Set[str]] = {
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
}
DANGER_METHODS_BY_TYPE: Dict[str, Set[str]] = {
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
    },
}
