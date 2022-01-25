from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f203.cloudformation import (
    _cfn_public_buckets,
)
from lib_path.f203.terraform import (
    _tfm_public_buckets,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from parse_hcl2.loader import (
    load_blocking as load_terraform,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    List,
)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def cfn_public_buckets(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    # cfn_nag F14 S3 Bucket should not have a public read-write acl
    # cfn_nag W31 S3 Bucket likely should not have a public read acl
    return _cfn_public_buckets(content=content, path=path, template=template)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def tfm_public_buckets(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    return _tfm_public_buckets(
        content=content,
        path=path,
        model=model,
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    coroutines: List[Awaitable[Vulnerabilities]] = []
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()

        for template in load_templates_blocking(content, fmt=file_extension):
            coroutines.append(cfn_public_buckets(content, path, template))

    elif file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])

        coroutines.append(tfm_public_buckets(content, path, model))

    return coroutines
