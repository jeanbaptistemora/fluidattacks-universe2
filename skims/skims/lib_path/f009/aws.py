# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    get_vulnerabilities_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from pyparsing import (
    Regex,
)


def aws_credentials(content: str, path: str) -> Vulnerabilities:
    return get_vulnerabilities_blocking(
        content=content,
        description_key="src.lib_path.f009.aws_credentials.description",
        grammar=Regex(r"AKIA[A-Z0-9]{16}"),
        path=path,
        method=MethodsEnum.AWS_CREDENTIALS,
    )
