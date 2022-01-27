from aws.model import (
    AWSElbV2,
)
from lib_path.common import (
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    DeveloperEnum,
    FindingEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_elb2_load_listeners,
)
from typing import (
    Any,
    Iterator,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_elb2_uses_insecure_security_policy_iterate_vulnerabilities(
    file_ext: str,
    listeners_iterator: Iterator[Union[AWSElbV2, Node]],
) -> Iterator[Union[AWSElbV2, Node]]:
    for listener in listeners_iterator:
        acceptable = (
            "ELBSecurityPolicy-2016-08",
            "ELBSecurityPolicy-TLS-1-1-2017-01",
            "ELBSecurityPolicy-FS-2018-06",
            "ELBSecurityPolicy-TLS-1-2-Ext-2018-06",
        )
        ssl_policy = listener.raw.get("SslPolicy", "")
        if ssl_policy not in acceptable:
            ssl_pol_node = get_node_by_keys(listener, ["SslPolicy"])
            if isinstance(ssl_pol_node, Node):
                yield ssl_pol_node
            else:
                yield AWSElbV2(
                    column=listener.start_column,
                    data=listener.data,
                    line=get_line_by_extension(listener.start_line, file_ext),
                )


def cfn_elb2_uses_insecure_security_policy(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F070.value.cwe},
        description_key="src.lib_path.f070.elb2_uses_insecure_security_policy",
        finding=FindingEnum.F070,
        iterator=get_cloud_iterator(
            _cfn_elb2_uses_insecure_security_policy_iterate_vulnerabilities(
                file_ext=file_ext,
                listeners_iterator=iter_elb2_load_listeners(template=template),
            )
        ),
        path=path,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
    )
