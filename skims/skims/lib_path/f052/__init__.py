# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    EXTENSIONS_JAVA_PROPERTIES,
    SHIELD_BLOCKING,
)
from lib_path.f052.java import (
    java_properties_missing_ssl,
    java_properties_weak_cipher_suite,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_java_properties_missing_ssl(
    content: str, path: str
) -> Vulnerabilities:
    return java_properties_missing_ssl(content=content, path=path)


@SHIELD_BLOCKING
def run_java_properties_weak_cipher_suite(
    content: str, path: str
) -> Vulnerabilities:
    return java_properties_weak_cipher_suite(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    if file_extension in EXTENSIONS_JAVA_PROPERTIES:
        content = content_generator()
        return (
            run_java_properties_missing_ssl(content, path),
            run_java_properties_weak_cipher_suite(content, path),
        )

    return ()
