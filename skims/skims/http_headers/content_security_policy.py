from http_headers.common import (
    get_header_value_delimiter,
)
from http_headers.types import (
    ContentSecurityPolicyHeader,
)
from operator import (
    methodcaller,
)


def _is_content_security_policy(name: str) -> bool:
    return name.lower() == "content-security-policy"


def parse(line: str) -> ContentSecurityPolicyHeader | None:
    # Content-Security-Policy: <policy-directive>; <policy-directive>

    portions: list[str] = line.split(":", maxsplit=1)
    portions = list(map(methodcaller("strip"), portions))

    # Get the name in `name: value`
    name = portions.pop(0)

    if not _is_content_security_policy(name):
        return None

    # Get the value in `name: value`
    directives: dict[str, list[str]] = {}
    if portions:
        value = portions.pop(0).lower()

        values = value.split(get_header_value_delimiter(value))
        values = list(map(methodcaller("strip"), values))
        values = list(filter(None, values))

        for value in values:
            components = value.split(" ")
            components = list(map(methodcaller("strip"), components))
            components = list(filter(None, components))

            if components:
                # The directive could have different forms
                if components[0].endswith(":"):
                    # "frame-ancestors:"
                    components[0] = components[0][:-1]
                elif "=" in components[0] and len(components) == 1:
                    # "upgrade-insecure-requests=1"
                    components = components[0].split("=")

                # Only the first directive is taken into account
                # Later directives do not override the previous ones
                directives.setdefault(components[0], components[1:])

    return ContentSecurityPolicyHeader(
        name=name,
        directives=directives,
    )
