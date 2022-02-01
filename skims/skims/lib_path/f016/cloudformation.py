from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from lib_path.f016.constants import (
    VULNERABLE_MIN_PROT_VERSIONS,
    VULNERABLE_ORIGIN_SSL_PROTOCOLS,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_cloudfront_distributions,
)
from typing import (
    Any,
    Iterator,
    List,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def _helper_insecure_protocols(
    orig_ssl_prots: Node,
    vulnerable_origin_ssl_protocols: List[str],
) -> Iterator[Node]:
    for ssl_prot in orig_ssl_prots.data:
        if ssl_prot.raw in vulnerable_origin_ssl_protocols:
            yield ssl_prot


def _cfn_content_over_insecure_protocols_iterate_vulnerabilities(
    distributions_iterator: Iterator[Union[Any, Node]]
) -> Iterator[Union[Any, Node]]:

    for dist in distributions_iterator:
        dist_config = dist.inner["DistributionConfig"]
        if isinstance(dist_config, Node):
            min_prot_ver = get_node_by_keys(
                dist_config, ["ViewerCertificate", "MinimumProtocolVersion"]
            )
            if (
                isinstance(min_prot_ver, Node)
                and min_prot_ver.raw in VULNERABLE_MIN_PROT_VERSIONS
            ):
                yield min_prot_ver
            origins = get_node_by_keys(dist_config, ["Origins"])
            if isinstance(origins, Node):
                for origin in origins.data:
                    orig_ssl_prots = get_node_by_keys(
                        origin, ["CustomOriginConfig", "OriginSSLProtocols"]
                    )
                    if isinstance(orig_ssl_prots, Node):
                        yield from _helper_insecure_protocols(
                            orig_ssl_prots, VULNERABLE_ORIGIN_SSL_PROTOCOLS
                        )


def cfn_serves_content_over_insecure_protocols(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f016.serves_content_over_insecure_protocols"
        ),
        iterator=get_cloud_iterator(
            _cfn_content_over_insecure_protocols_iterate_vulnerabilities(
                distributions_iterator=iter_cloudfront_distributions(
                    template=template
                )
            )
        ),
        path=path,
        method=MethodsEnum.CFN_INSEC_PROTO,
    )
