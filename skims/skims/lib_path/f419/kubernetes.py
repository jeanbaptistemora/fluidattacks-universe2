# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    get_all_values_from_nested_dict,
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from typing import (
    Any,
    Iterator,
)


def _k8s_check_audit_flag(
    template: Any,
) -> Iterator[Any]:
    if (api_version := template.inner.get("apiVersion")) and (
        values := list(get_all_values_from_nested_dict(template.raw))
    ):
        exist_audit_flag = False
        for value in values:
            if "--audit-log-path" in value:
                exist_audit_flag = True

        if not exist_audit_flag:
            yield api_version


def k8s_check_audit_flag(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=("lib_path.f419.k8s_check_audit_flag"),
        iterator=get_cloud_iterator(_k8s_check_audit_flag(template=template)),
        path=path,
        method=MethodsEnum.K8S_CHECK_AUDIT_FLAG,
    )
