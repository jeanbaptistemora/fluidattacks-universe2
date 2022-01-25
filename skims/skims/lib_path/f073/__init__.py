from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f073.cloudformation import (
    cfn_rds_is_publicly_accessible,
)
from lib_path.f073.terraform import (
    tfm_db_cluster_publicly_accessible,
    tfm_db_instance_publicly_accessible,
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
def run_cfn_rds_is_publicly_accessible(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_rds_is_publicly_accessible(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_db_cluster_publicly_accessible(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_db_cluster_publicly_accessible(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_db_instance_publicly_accessible(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_db_instance_publicly_accessible(
        content=content, path=path, model=model
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
            coroutines.append(
                run_cfn_rds_is_publicly_accessible(content, path, template)
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])

        coroutines.append(
            run_tfm_db_cluster_publicly_accessible(content, path, model)
        )
        coroutines.append(
            run_tfm_db_instance_publicly_accessible(content, path, model)
        )

    return coroutines
