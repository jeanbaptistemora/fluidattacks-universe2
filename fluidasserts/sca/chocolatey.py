# -*- coding: utf-8 -*-

"""Software Composition Analysis for Chocolatey packages."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts.helper import sca
from fluidasserts.utils.decorators import track, level, notify

PKG_MNGR = 'chocolatey'


@notify
@level('high')
@track
def package_has_vulnerabilities(
        package: str, version: str = None, retry: bool = True) -> bool:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    """
    return sca.process_requirement(PKG_MNGR, package, version, retry)
