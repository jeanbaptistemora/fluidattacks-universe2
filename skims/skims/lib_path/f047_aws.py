# Standard library
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Tuple,
)
from contextlib import suppress

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)
from metaloaders.model import (
    Node,
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities_from_iterator,
    EXTENSIONS_CLOUDFORMATION,
    SHIELD,
)
from parse_cfn.structure import (
    iter_ec2_ingress_egress,
)
from parse_cfn.loader import (
    load_templates,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)
from zone import (
    t,
)


def _create_vulns(
    content: str,
    description_key: str,
    path: str,
    ports_iterator: Iterator[Node, ],
) -> Tuple[Vulnerability, ...]:
    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        cwe={'275'},
        description=t(
            key=description_key,
            path=path,
        ),
        finding=FindingEnum.F047_AWS,
        iterator=((
            stmt.start_line,
            stmt.start_column,
        ) for stmt in ports_iterator),
        path=path,
    )


def _range_port_iter_vulnerabilities(
        rules_iterator: Iterator[Node]) -> Iterator[Node]:
    for rule in rules_iterator:
        rule_raw = rule.raw
        with suppress(ValueError):
            if int(rule_raw['FromPort']) != int(rule_raw['ToPort']):
                yield rule.inner['FromPort']
                yield rule.inner['ToPort']


def _cnf_unrestricted_ports(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f047_aws.unrestricted_ports',
        path=path,
        ports_iterator=_range_port_iter_vulnerabilities(
            rules_iterator=iter_ec2_ingress_egress(
                template=template,
                ingress=True,
                egress=True,
            )))


@CACHE_ETERNALLY
@SHIELD
async def cnf_unrestricted_ports(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
    # cfn_nag W27 Security Groups found ingress with port range instead of just
    # a single port
    # cfn_nag W29 Security Groups found egress with port range instead of just
    # a single port
    return await in_process(
        _cnf_unrestricted_ports,
        content=content,
        path=path,
        template=template,
    )


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(content=content,
                                             fmt=file_extension):
            coroutines.append(cnf_unrestricted_ports(
                content=content,
                path=path,
                template=template,
            ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
