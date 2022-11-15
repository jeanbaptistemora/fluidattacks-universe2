# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f153.conf_files import (
    xml_accept_header,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_xml_accept_header(
    content: str,
    path: str,
) -> Vulnerabilities:
    return xml_accept_header(
        content=content,
        path=path,
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in ("config", "xml", "jmx"):
        content = content_generator()
        results = (
            *results,
            run_xml_accept_header(content, path),
        )

    return results
