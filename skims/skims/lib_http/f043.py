# Standard librar
from itertools import (
    chain,
)
from typing import (
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Type,
)

# Local libraries
from http_headers import (
    as_string,
    content_security_policy,
    from_url,
    referrer_policy,
    strict_transport_security,
)
from http_headers.types import (
    ContentSecurityPolicyHeader,
    ReferrerPolicyHeader,
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


FINDING_HEADERS: Dict[core_model.FindingEnum, str] = {
    core_model.FindingEnum.F043_DAST_CSP: 'Content-Security-Policy',
    core_model.FindingEnum.F043_DAST_RP: 'Referrer-Policy',
    core_model.FindingEnum.F043_DAST_STS: 'Strict-Transport-Security',
}


def _create_vulns(
    descriptions: List[str],
    finding: core_model.FindingEnum,
    header: Optional[Header],
    headers_raw: Dict[str, str],
    url: str,
) -> core_model.Vulnerabilities:
    return tuple(
        core_model.Vulnerability(
            finding=finding,
            kind=core_model.VulnerabilityKindEnum.INPUTS,
            state=core_model.VulnerabilityStateEnum.OPEN,
            stream='Query,response,headers',
            what=serialize_namespace_into_vuln(
                kind=core_model.VulnerabilityKindEnum.INPUTS,
                namespace=CTX.config.namespace,
                what=url,
            ),
            where=FINDING_HEADERS[finding],
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=('644',),
                description=t(f'lib_http.f043.{description}'),
                snippet=as_string.snippet(
                    url=url,
                    header=header.name if header else None,
                    headers=headers_raw,
                ),
            ),
        )
        for description in descriptions
        if description
    )


def _content_security_policy_script_src(
    descs: List[str],
    header: Header,
) -> None:
    if _ := header.directives.get('script-src'):
        pass
    elif _ := header.directives.get('default-src'):
        pass
    else:
        descs.append('content_security_policy.missing_script_src')


def _content_security_policy(
    url: str,
    headers: Dict[Type[Header], Header],
    headers_raw: Dict[str, str],
) -> core_model.Vulnerabilities:
    descs: List[str] = []
    header: Optional[Header] = None

    if header := headers.get(ContentSecurityPolicyHeader):
        _content_security_policy_script_src(descs, header)
    else:
        descs.append('content_security_policy.missing')

    return _create_vulns(
        descriptions=descs,
        finding=core_model.FindingEnum.F043_DAST_CSP,
        header=header,
        headers_raw=headers_raw,
        url=url,
    )


def _referrer_policy(
    url: str,
    headers: Dict[Type[Header], Header],
    headers_raw: Dict[str, str],
) -> core_model.Vulnerabilities:
    desc, header = '', None

    if header := headers.get(ReferrerPolicyHeader):
        for value in header.values:
            # Some header values may be out of the spec or experimental
            # We won't take them into account as some browsers won't
            # support them. The spec says that browsers should read the next
            # value in the comma separated list
            if value in {
                'no-referrer',
                'no-referrer-when-downgrade',
                'origin',
                'origin-when-cross-origin',
                'same-origin',
                'strict-origin',
                'strict-origin-when-cross-origin',
                'unsafe-url',
            }:
                desc = (
                    ''
                    if value in {
                        'no-referrer',
                        'same-origin',
                        'strict-origin',
                        'strict-origin-when-cross-origin',
                    }
                    else 'referrer_policy.weak'
                )
                break
        else:
            desc = 'referrer_policy.weak'

    else:
        desc = 'referrer_policy.missing'

    return _create_vulns(
        descriptions=[desc],
        finding=core_model.FindingEnum.F043_DAST_RP,
        header=header,
        headers_raw=headers_raw,
        url=url,
    )


def _strict_transport_security(
    url: str,
    headers: Dict[Type[Header], Header],
    headers_raw: Dict[str, str],
) -> core_model.Vulnerabilities:
    desc, header = '', None

    if val := headers.get(StrictTransportSecurityHeader):
        if val.max_age < 31536000:
            desc = 'strict_transport_security.short_max_age'
    else:
        desc = 'strict_transport_security.missing'

    return _create_vulns(
        descriptions=[desc],
        finding=core_model.FindingEnum.F043_DAST_STS,
        header=header,
        headers_raw=headers_raw,
        url=url,
    )


async def http_headers_configuration(url: str) -> core_model.Vulnerabilities:
    headers_raw = await from_url.get('GET', url)
    headers_parsed: Dict[Type[Header], Header] = {
        type(header_parsed): header_parsed
        for header_raw_name, header_raw_value in headers_raw.items()
        for line in [f'{header_raw_name}: {header_raw_value}']
        for header_parsed in [
            content_security_policy.parse(line),
            referrer_policy.parse(line),
            strict_transport_security.parse(line),
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
    core_model.FindingEnum.F043_DAST_CSP: _content_security_policy,
    core_model.FindingEnum.F043_DAST_RP: _referrer_policy,
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
