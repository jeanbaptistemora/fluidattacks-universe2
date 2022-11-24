from aws.model import (
    AWSKmsKey,
)
from lib_path.common import (
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.structure.aws import (
    iter_aws_kms_key,
)
from parse_hcl2.tokens import (
    Attribute,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_kms_key_is_key_rotation_absent_or_disabled_iter_vulns(
    resource_iterator: Iterator[AWSKmsKey],
) -> Iterator[Union[Attribute, AWSKmsKey]]:
    for res in resource_iterator:
        en_key_rot = get_attribute(res.data, "enable_key_rotation")
        key_spec = get_attribute(res.data, "customer_master_key_spec")
        if key_spec is None or key_spec.val != "SYMMETRIC_DEFAULT":
            continue
        if en_key_rot is None:
            yield res
        elif en_key_rot.val in FALSE_OPTIONS:
            yield en_key_rot


def tfm_kms_key_is_key_rotation_absent_or_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f396.tfm_kms_key_is_key_rotation_absent_or_disabled"
        ),
        iterator=get_cloud_iterator(
            _tfm_kms_key_is_key_rotation_absent_or_disabled_iter_vulns(
                resource_iterator=iter_aws_kms_key(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_KMS_KEY_ROTATION_DISABLED,
    )
