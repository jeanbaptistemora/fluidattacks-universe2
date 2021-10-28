from aioextensions import (
    in_process,
)
from aws.model import (
    AWSCloudfrontDistribution,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    get_vulnerabilities_from_aws_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_cloudfront_distributions,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure import (
    get_argument,
    get_attribute_by_block,
    get_block_attribute,
    iter_aws_cloudfront_distribution,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Union,
)
from utils.function import (
    get_node_by_keys,
    TIMEOUT_1MIN,
)


def helper_insecure_protocols(
    orig_ssl_prots: Node,
    vulnerable_origin_ssl_protocols: List[str],
) -> Iterator[Node]:
    for ssl_prot in orig_ssl_prots.data:
        if ssl_prot.raw in vulnerable_origin_ssl_protocols:
            yield ssl_prot


def cfn_content_over_insecure_protocols_iterate_vulnerabilities(
    distributions_iterator: Iterator[Union[Any, Node]]
) -> Iterator[Union[Any, Node]]:
    vulnerable_origin_ssl_protocols = ["SSLv3", "TLSv1", "TLSv1.1"]
    vulnerable_min_prot_versions = [
        "SSLv3",
        "TLSv1",
        "TLSv1_2016",
        "TLSv1.1_2016",
    ]
    for dist in distributions_iterator:
        dist_config = dist.inner["DistributionConfig"]
        if isinstance(dist_config, Node):
            min_prot_ver = get_node_by_keys(
                dist_config, ["ViewerCertificate", "MinimumProtocolVersion"]
            )
            if (
                isinstance(min_prot_ver, Node)
                and min_prot_ver.raw in vulnerable_min_prot_versions
            ):
                yield min_prot_ver
            origins = get_node_by_keys(dist_config, ["Origins"])
            if isinstance(origins, Node):
                for origin in origins.data:
                    orig_ssl_prots = get_node_by_keys(
                        origin, ["CustomOriginConfig", "OriginSSLProtocols"]
                    )
                    if isinstance(orig_ssl_prots, Node):
                        yield from helper_insecure_protocols(
                            orig_ssl_prots, vulnerable_origin_ssl_protocols
                        )


def tfm_content_over_insecure_protocols_iterate_vulnerabilities(
    buckets_iterator: Iterator[Union[AWSCloudfrontDistribution, Node]]
) -> Iterator[Union[Any, Node]]:
    vulnerable_origin_ssl_protocols = ["SSLv3", "TLSv1", "TLSv1.1"]
    vulnerable_min_prot_versions = [
        "SSLv3",
        "TLSv1",
        "TLSv1_2016",
        "TLSv1.1_2016",
    ]
    for bucket in buckets_iterator:
        if isinstance(bucket, AWSCloudfrontDistribution):
            if v_cert := get_argument(
                key="viewer_certificate",
                body=bucket.data,
            ):
                if min_prot := get_block_attribute(
                    v_cert, "minimum_protocol_version"
                ):
                    if any(
                        True
                        for protocol in vulnerable_min_prot_versions
                        if protocol == min_prot.val
                    ):
                        yield min_prot
            if origin := get_argument(
                key="origin",
                body=bucket.data,
            ):
                if ssl_prot := get_attribute_by_block(
                    block=origin,
                    namespace="custom_origin_config",
                    key="origin_ssl_protocols",
                ):
                    if (
                        len(
                            set(ssl_prot.val).intersection(
                                vulnerable_origin_ssl_protocols
                            )
                        )
                        > 0
                    ):
                        yield ssl_prot


def _cfn_serves_content_over_insecure_protocols(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f016.serves_content_over_insecure_protocols"
        ),
        finding=core_model.FindingEnum.F016,
        path=path,
        statements_iterator=(
            cfn_content_over_insecure_protocols_iterate_vulnerabilities(
                distributions_iterator=iter_cloudfront_distributions(
                    template=template
                )
            )
        ),
    )


def _tfm_serves_content_over_insecure_protocols(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f016.serves_content_over_insecure_protocols"
        ),
        finding=core_model.FindingEnum.F016,
        path=path,
        statements_iterator=(
            tfm_content_over_insecure_protocols_iterate_vulnerabilities(
                buckets_iterator=iter_aws_cloudfront_distribution(model=model)
            )
        ),
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_serves_content_over_insecure_protocols(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_serves_content_over_insecure_protocols,
        content=content,
        path=path,
        template=template,
    )


async def tfm_serves_content_over_insecure_protocols(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _tfm_serves_content_over_insecure_protocols,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_serves_content_over_insecure_protocols(
                    content=content,
                    path=path,
                    template=template,
                )
            )
    if file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            tfm_serves_content_over_insecure_protocols(
                content=content,
                path=path,
                model=model,
            )
        )

    return coroutines
