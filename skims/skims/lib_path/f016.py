from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
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


def _serves_content_over_insecure_protocols_iterate_vulnerabilities(
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
            _serves_content_over_insecure_protocols_iterate_vulnerabilities(
                distributions_iterator=iter_cloudfront_distributions(
                    template=template
                )
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

    return coroutines
