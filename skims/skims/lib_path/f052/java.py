# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_java_properties import (
    load as load_java_properties,
)
from typing import (
    Iterator,
    Set,
    Tuple,
)
from utils.crypto import (
    is_iana_cipher_suite_vulnerable,
    is_open_ssl_cipher_suite_vulnerable,
)


def java_properties_missing_ssl(content: str, path: str) -> Vulnerabilities:
    missing_ssl_key: str = "ibm.mq.use_ssl"
    missing_ssl_values: Set[str] = {"false"}

    def _iterate_vulnerabilities() -> Iterator[Tuple[int, int]]:
        for line_no, (key, val) in load_java_properties(content).items():
            if key == missing_ssl_key and val in missing_ssl_values:
                yield line_no, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f052.java_properties_missing_ssl",
        iterator=_iterate_vulnerabilities(),
        path=path,
        method=MethodsEnum.JAVA_PROP_MISSING_SSL,
    )


def java_properties_weak_cipher_suite(
    content: str, path: str
) -> Vulnerabilities:
    weak_cipher_suite: str = "ibm.mq.cipher.suite"

    def _iterate_vulnerabilities() -> Iterator[Tuple[int, int]]:
        for line_no, (key, val) in load_java_properties(content).items():
            if key == weak_cipher_suite and (
                is_iana_cipher_suite_vulnerable(val)
                or is_open_ssl_cipher_suite_vulnerable(val)
            ):
                yield line_no, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f052.java_properties_weak_cipher_suite",
        iterator=_iterate_vulnerabilities(),
        path=path,
        method=MethodsEnum.JAVA_PROP_WEAK_CIPHER,
    )
