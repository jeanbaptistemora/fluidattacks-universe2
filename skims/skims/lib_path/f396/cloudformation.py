from aws.model import (
    AWSKmsKey,
)
from lib_path.common import (
    FALSE_OPTIONS,
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_kms_keys,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _cfn_kms_key_is_key_rotation_absent_or_disabled_iter_vulns(
    file_ext: str,
    keys_iterator: Iterator[Node],
) -> Iterator[Union[AWSKmsKey, Node]]:
    key_spec_symmetric = "SYMMETRIC_DEFAULT"
    for key in keys_iterator:
        en_key_rot = key.inner.get("EnableKeyRotation")
        key_spec = key.raw.get("KeySpec", key_spec_symmetric)
        if key_spec == key_spec_symmetric:
            if not isinstance(en_key_rot, Node):
                yield AWSKmsKey(
                    column=key.start_column,
                    data=key.data,
                    line=get_line_by_extension(key.start_line, file_ext),
                )
            elif en_key_rot.raw in FALSE_OPTIONS:
                yield en_key_rot


def cfn_kms_key_is_key_rotation_absent_or_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f396.kms_key_is_key_rotation_absent_or_disabled"
        ),
        iterator=get_cloud_iterator(
            _cfn_kms_key_is_key_rotation_absent_or_disabled_iter_vulns(
                file_ext=file_ext,
                keys_iterator=iter_kms_keys(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_KMS_KEY_ROTATION_DISABLED,
    )
