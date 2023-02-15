from aws.model import (
    AWSS3Bucket,
    AWSS3SSEConfig,
)
from collections.abc import (
    Iterator,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_argument,
)
from parse_hcl2.structure.aws import (
    iter_s3_buckets as tfm_iter_s3_buckets,
    iter_s3_sse_configuration as tfm_iter_s3_sse_configuration,
)
from typing import (
    Any,
)


def _tfm_unencrypted_buckets_iterate_vulnerabilities(
    buckets_iterator: Iterator[AWSS3Bucket],
    sse_config_iterator: Iterator[AWSS3SSEConfig],
) -> Iterator[AWSS3Bucket]:
    sse_configs = list(sse_config_iterator)
    for bucket in buckets_iterator:
        if not get_argument(
            body=bucket.data,
            key="server_side_encryption_configuration",
        ):
            has_sse_config: bool = False
            for sse_config in sse_configs:
                if (
                    bucket.name is not None
                    and bucket.tf_reference is not None
                    and (
                        sse_config.bucket
                        in (bucket.name, f"{bucket.tf_reference}.id")
                    )
                ):
                    has_sse_config = True
                    break
            if not has_sse_config:
                yield bucket


def tfm_unencrypted_buckets(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f099.unencrypted_buckets",
        iterator=get_cloud_iterator(
            _tfm_unencrypted_buckets_iterate_vulnerabilities(
                buckets_iterator=tfm_iter_s3_buckets(model=model),
                sse_config_iterator=tfm_iter_s3_sse_configuration(model=model),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_UNENCRYPTED_BUCKETS,
    )
