# -*- coding: utf-8 -*-

"""Software Composition Analysis for Linux packages."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts import Result
from fluidasserts import HIGH
from fluidasserts.helper import sca
from fluidasserts.utils.decorators import api

PKG_MNGR = 'rpm'


@api(risk=HIGH)
def package_has_vulnerabilities(
        package: str, version: str = None, retry: bool = True) -> Result:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    """
    reqs = set([(None, package, version)])
    return sca.process_requirements(PKG_MNGR, None, reqs, retry)
