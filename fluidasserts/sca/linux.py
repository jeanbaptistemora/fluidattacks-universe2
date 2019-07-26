# -*- coding: utf-8 -*-

"""Software Composition Analysis for Linux packages."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts.helper import sca
from fluidasserts.utils.decorators import track, level, notify

PACKAGE_MANAGER = 'rpm'


@notify
@level('high')
@track
def package_has_vulnerabilities(package: str, version: str = None) -> bool:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    """
    return sca.get_vulns_from_ossindex(PACKAGE_MANAGER, package, version)
