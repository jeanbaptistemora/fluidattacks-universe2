# Standard librar
from itertools import (
    chain,
)
from typing import (
    Awaitable,
    Callable,
    Dict,
    List,
    Type,
)

# Local libraries
from http_headers import (
    as_string,
    from_url,
    strict_transport_security,
)
from http_headers.types import (
    StrictTransportSecurityHeader,
)
from http_headers.types import (
    Header,
)
from model import (
    core_model,
)
from utils.ctx import (
    CTX,
)
from utils.encodings import (
    serialize_namespace_into_vuln,
)
from zone import (
    t,
)


def _strict_transport_security(
    url: str,
    headers: Dict[Type[Header], Header],
    headers_raw: Dict[str, str],
) -> core_model.Vulnerabilities:
    desc: str = ''

    if val := headers.get(StrictTransportSecurityHeader):
        if val.max_age < 31536000:
            desc = 'lib_http.f043.strict_transport_security.short_max_age'
    else:
        desc = 'lib_http.f043.strict_transport_security.missing'

    return (
        core_model.Vulnerability(
            finding=core_model.FindingEnum.F043_DAST_STS,
            kind=core_model.VulnerabilityKindEnum.INPUTS,
            state=core_model.VulnerabilityStateEnum.OPEN,
            stream='Query,response,headers',
            what=serialize_namespace_into_vuln(
                kind=core_model.VulnerabilityKindEnum.INPUTS,
                namespace=CTX.config.namespace,
                what=url,
            ),
            where='Strict-Transport-Security',
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=('644',),
                description=t(desc),
                snippet=as_string.snippet(
                    url=url,
                    header=val.name if val else None,
                    headers=headers_raw,
                ),
            ),
        ),
    ) if desc else ()


async def http_headers_configuration(url: str) -> core_model.Vulnerabilities:
    headers_raw = await from_url.get('GET', url)
    headers_parsed: Dict[Type[Header], Header] = {
        type(header_parsed): header_parsed
        for header_raw_name, header_raw_value in headers_raw.items()
        for line in [f'{header_raw_name}: {header_raw_value}']
        for header_parsed in [
            strict_transport_security.parse(line)
        ]
        if header_parsed is not None
    }

    return tuple(chain.from_iterable((
        check(url, headers_parsed, headers_raw)
        for finding, check in CHECKS.items()
        if finding in CTX.config.checks
    )))


CHECKS: Dict[
    core_model.FindingEnum,
    Callable[
        [str, Dict[Type[Header], Header], Dict[str, str]],
        core_model.Vulnerabilities,
    ],
] = {
    core_model.FindingEnum.F043_DAST_STS: _strict_transport_security,
}


def analyze(
    url: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = [
        http_headers_configuration(url),
    ]

    return coroutines


def should_run() -> bool:
    return any(finding in CTX.config.checks for finding in CHECKS)
