from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f400.cloudformation import (
    cfn_ec2_monitoring_disabled,
    cfn_elb2_has_access_logs_s3_disabled,
    cfn_elb_has_access_logging_disabled,
    cfn_trails_not_multiregion,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from typing import (
    Any,
)


@SHIELD_BLOCKING
def run_cfn_elb_has_access_logging_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_elb_has_access_logging_disabled(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_trails_not_multiregion(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_trails_not_multiregion(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_elb2_has_access_logs_s3_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_elb2_has_access_logs_s3_disabled(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_ec2_monitoring_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_monitoring_disabled(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()

        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_cfn_elb_has_access_logging_disabled(
                    content, file_extension, path, template
                ),
                run_cfn_trails_not_multiregion(
                    content, file_extension, path, template
                ),
                run_cfn_elb2_has_access_logs_s3_disabled(
                    content, file_extension, path, template
                ),
                run_cfn_ec2_monitoring_disabled(
                    content, file_extension, path, template
                ),
            )

    return results
