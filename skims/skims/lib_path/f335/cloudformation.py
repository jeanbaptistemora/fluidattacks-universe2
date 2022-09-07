# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aws.model import (
    AWSS3Bucket,
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
    iter_s3_buckets,
)
from typing import (
    Any,
    Iterator,
    Union,
)
from utils.function import (
    get_node_by_keys,
)


def _cfn_s3_bucket_versioning_disabled_iterate_vulnerabilities(
    file_ext: str,
    res_iterator: Iterator[Node],
) -> Iterator[Union[AWSS3Bucket, Node]]:
    for res in res_iterator:
        bck_config = get_node_by_keys(
            res, ["VersioningConfiguration", "Status"]
        )
        if bck_config is None:
            yield AWSS3Bucket(
                column=res.start_column,
                data=res.data,
                line=get_line_by_extension(res.start_line, file_ext),
            )
        elif bck_config.raw != "Enabled":
            yield bck_config


def cfn_s3_bucket_versioning_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f335.cfn_s3_bucket_versioning_disabled",
        iterator=get_cloud_iterator(
            _cfn_s3_bucket_versioning_disabled_iterate_vulnerabilities(
                file_ext=file_ext,
                res_iterator=iter_s3_buckets(template=template),
            )
        ),
        path=path,
        method=MethodsEnum.CFN_S3_VERSIONING_DISABLED,
    )
