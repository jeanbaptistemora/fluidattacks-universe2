# Standard libraryes
from operator import (
    methodcaller,
)
from typing import (
    Dict,
    List,
    Optional,
)

# Third party libraries
from http_headers.types import (
    ContentSecurityPolicyHeader,
)


def _is_content_security_policy(name: str) -> bool:
    return name.lower() == 'content-security-policy'


def parse(line: str) -> Optional[ContentSecurityPolicyHeader]:
    # Content-Security-Policy: <policy-directive>; <policy-directive>

    portions: List[str] = line.split(':', maxsplit=1)
    portions = list(map(methodcaller('strip'), portions))

    # Get the name in `name: value`
    name = portions.pop(0)

    if not _is_content_security_policy(name):
        return None

    # Get the value in `name: value`
    directives: Dict[str, List[str]] = {}
    if portions:
        values = portions.pop(0).lower().split(';')
        values = list(map(methodcaller('strip'), values))
        values = list(filter(None, values))

        for value in values:
            components = value.split(' ')
            components = list(map(methodcaller('strip'), components))
            components = list(filter(None, components))

            if components:
                # Only the first directive is taken into account
                # Later directives do not override the previous ones
                directives.setdefault(components[0], components[1:])

    return ContentSecurityPolicyHeader(
        name=name,
        directives=directives,
    )
