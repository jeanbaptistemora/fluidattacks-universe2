from aws.model import (
    AWSS3Bucket,
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
    iter_s3_bucket_policies,
    iter_s3_buckets,
)
from typing import (
    Any,
    Iterator,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_bucket_policy_has_server_side_encryption_disabled_iter_vulns(
    policies_iterator: Iterator[Node],
) -> Iterator[Node]:
    for policy in policies_iterator:
        statements = get_node_by_keys(policy, ["PolicyDocument", "Statement"])
        if not statements:
            continue
        for statement in statements.data:
            effect = statement.raw.get("Effect", "")
            sse = get_node_by_keys(
                statement,
                ["Condition", "Null", "s3:x-amz-server-side-encryption"],
            )
            if (
                (
                    sse := get_node_by_keys(
                        statement,
                        [
                            "Condition",
                            "Null",
                            "s3:x-amz-server-side-encryption",
                        ],
                    )
                )
                and (isinstance(sse, Node))
                and ((effect == "Allow" and sse.raw in FALSE_OPTIONS))
            ):
                yield sse


def _cfn_unencrypted_buckets_iterate_vulnerabilities(
    file_ext: str,
    buckets_iterator: Iterator[Node],
) -> Iterator[AWSS3Bucket]:
    for bucket in buckets_iterator:
        bck_encrypt = bucket.inner.get("BucketEncryption")
        if not isinstance(bck_encrypt, Node):
            yield AWSS3Bucket(
                column=bucket.start_column,
                data=bucket.data,
                line=get_line_by_extension(bucket.start_line, file_ext),
            )


def cfn_bucket_policy_has_server_side_encryption_disabled(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "src.lib_path.f099.bckp_has_server_side_encryption_disabled"
        ),
        iterator=get_cloud_iterator(
            _cfn_bucket_policy_has_server_side_encryption_disabled_iter_vulns(
                policies_iterator=iter_s3_bucket_policies(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_POLICY_SERVER_ENCRYP_DISABLED,
    )


def cfn_unencrypted_buckets(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f099.unencrypted_buckets",
        iterator=get_cloud_iterator(
            _cfn_unencrypted_buckets_iterate_vulnerabilities(
                file_ext=file_ext,
                buckets_iterator=iter_s3_buckets(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_UNENCRYPTED_BUCKETS,
    )
