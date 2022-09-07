# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
)
from parse_hcl2.structure.aws import (
    iter_s3_buckets,
)
from typing import (
    Any,
    Iterator,
    Union,
)


def _tfm_public_buckets_iterate_vulnerabilities(
    resource_iterator: Iterator[Any],
) -> Iterator[Union[Any, Node]]:
    for resource in resource_iterator:
        acl = get_attribute(body=resource.data, key="acl")
        if acl and acl.val == "public-read-write":
            yield acl


def tfm_public_buckets(content: str, path: str, model: Any) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f203.public_buckets",
        iterator=get_cloud_iterator(
            _tfm_public_buckets_iterate_vulnerabilities(
                resource_iterator=iter_s3_buckets(model=model)
            )
        ),
        path=path,
        method=MethodsEnum.TFM_PUBLIC_BUCKETS,
    )
