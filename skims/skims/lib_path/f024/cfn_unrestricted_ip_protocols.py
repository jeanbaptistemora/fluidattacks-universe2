from contextlib import (
    suppress,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_ec2_ingress_egress,
)
from typing import (
    Any,
    Iterator,
)


def _protocol_iter_vulnerabilities(
    rules_iterator: Iterator[Node],
) -> Iterator[Node]:
    for rule in rules_iterator:
        rule_raw = rule.raw
        with suppress(ValueError, KeyError):
            if rule_raw["IpProtocol"] in ("-1", -1):
                yield rule.inner["IpProtocol"]


def cfn_unrestricted_ip_protocols(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F024.value.cwe},
        description_key="src.lib_path.f024_aws.unrestricted_protocols",
        finding=FindingEnum.F024,
        iterator=get_cloud_iterator(
            _protocol_iter_vulnerabilities(
                rules_iterator=iter_ec2_ingress_egress(
                    template=template,
                    ingress=True,
                    egress=True,
                )
            )
        ),
        path=path,
    )
