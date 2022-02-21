from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f400.cloudformation import (
    cfn_bucket_has_logging_conf_disabled,
    cfn_cf_distribution_has_logging_disabled,
    cfn_elb2_has_access_logs_s3_disabled,
    cfn_elb_has_access_logging_disabled,
    cfn_trails_not_multiregion,
)
from lib_path.f400.terraform import (
    tfm_ec2_monitoring_disabled,
    tfm_elb_logging_disabled,
    tfm_s3_buckets_logging_disabled,
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
    Callable,
    Tuple,
)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_bucket_has_logging_conf_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_bucket_has_logging_conf_disabled(
        content=content, file_ext=file_ext, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_elb_has_access_logging_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_elb_has_access_logging_disabled(
        content=content, file_ext=file_ext, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_cf_distribution_has_logging_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_cf_distribution_has_logging_disabled(
        content=content, file_ext=file_ext, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_trails_not_multiregion(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_trails_not_multiregion(
        content=content, file_ext=file_ext, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_elb2_has_access_logs_s3_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_elb2_has_access_logs_s3_disabled(
        content=content, file_ext=file_ext, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_elb_logging_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_elb_logging_disabled(content=content, path=path, model=model)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_s3_buckets_logging_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_s3_buckets_logging_disabled(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_ec2_monitoring_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ec2_monitoring_disabled(content=content, path=path, model=model)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()

        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_cfn_bucket_has_logging_conf_disabled(
                    content, file_extension, path, template
                ),
                run_cfn_elb_has_access_logging_disabled(
                    content, file_extension, path, template
                ),
                run_cfn_cf_distribution_has_logging_disabled(
                    content, file_extension, path, template
                ),
                run_cfn_trails_not_multiregion(
                    content, file_extension, path, template
                ),
                run_cfn_elb2_has_access_logs_s3_disabled(
                    content, file_extension, path, template
                ),
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])

        results = (
            *results,
            run_tfm_elb_logging_disabled(content, path, model),
            run_tfm_s3_buckets_logging_disabled(content, path, model),
            run_tfm_ec2_monitoring_disabled(content, path, model),
        )

    return results
