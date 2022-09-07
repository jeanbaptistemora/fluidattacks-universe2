# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Software Composition Analysis for Linux packages."""


# None


# None


from fluidasserts import (
    HIGH,
    SCA,
)
from fluidasserts.helper import (
    sca,
)
from fluidasserts.utils.decorators import (
    api,
)

PKG_MNGR = "rpm"


@api(risk=HIGH, kind=SCA)
def package_has_vulnerabilities(
    package: str, version: str = None, retry: bool = True
) -> tuple:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    :rtype: :class:`fluidasserts.Result`
    """
    reqs = set([(None, package, version)])
    return sca.process_requirements(PKG_MNGR, None, reqs, retry)
