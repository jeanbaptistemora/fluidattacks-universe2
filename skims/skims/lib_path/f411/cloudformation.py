from aws.model import (
    AWSSecretsManagerSecret,
)
from lib_path.common import (
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
    iter_secret_manager_secrets,
)
from typing import (
    Any,
    Iterator,
)


def _cfn_aws_secret_encrypted_without_kms_key_iter_vulns(
    file_ext: str,
    res_iterator: Iterator[Node],
) -> Iterator[AWSSecretsManagerSecret]:
    for res in res_iterator:
        if not res.inner.get("KmsKeyId"):
            yield AWSSecretsManagerSecret(
                column=res.start_column,
                data=res.data,
                line=get_line_by_extension(res.start_line, file_ext),
            )


def cfn_aws_secret_encrypted_without_kms_key(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "lib_path.f411.cfn_aws_secret_encrypted_without_kms_key"
        ),
        iterator=get_cloud_iterator(
            _cfn_aws_secret_encrypted_without_kms_key_iter_vulns(
                file_ext=file_ext,
                res_iterator=iter_secret_manager_secrets(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_AWS_SECRET_WITHOUT_KMS_KEY,
    )
