# -*- coding: utf-8 -*-

"""Software Composition Analysis for Chocolatey packages."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts import HIGH, SAST
from fluidasserts.helper import sca
from fluidasserts.utils.decorators import api

PKG_MNGR = 'chocolatey'


@api(risk=HIGH, kind=SAST)
def package_has_vulnerabilities(
        package: str, version: str = None, retry: bool = True) -> tuple:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    :rtype: :class:`fluidasserts.Result`
    """
    reqs = set([(None, package, version)])
    return sca.process_requirements(PKG_MNGR, None, reqs, retry)
