from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f409.cloudformation import (
    cfn_dynamodb_table_unencrypted,
)
from lib_path.f409.terraform import (
    tfm_aws_dynamodb_table_unencrypted,
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
from typing import (
    Any,
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_cfn_dynamodb_table_unencrypted(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_dynamodb_table_unencrypted(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_aws_dynamodb_table_unencrypted(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_aws_dynamodb_table_unencrypted(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    content = content_generator()
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_cfn_dynamodb_table_unencrypted(
                    content, file_extension, path, template
                ),
            )

    elif file_extension in EXTENSIONS_TERRAFORM:
        model = load_terraform(stream=content, default=[])
        results = (
            *results,
            run_tfm_aws_dynamodb_table_unencrypted(content, path, model),
        )

    return results
