# -*- coding: utf-8 -*-

"""This module allows to check ``APK`` vulnerabilities."""

# standard imports

# 3rd party imports

# local imports
from fluidasserts import show_open
from fluidasserts import show_close
from fluidasserts import show_unknown
from fluidasserts.helper.lang import analyze_apk
from fluidasserts.utils.decorators import track, level, notify


@notify
@level('low')
@track
def is_unsigned(apk_file: str) -> bool:
    """
    Check if the given APK file is signed.

    :param apk_file: Path to the image to be tested.
    """
    try:
        apk, _, _ = analyze_apk(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    if apk.is_signed():
        show_close('APK file is signed', details=dict(apk=apk_file))
        return False
    show_open('APK file is not signed', details=dict(apk=apk_file))
    return True


@notify
@level('low')
@track
def not_checks_for_root(apk_file: str) -> bool:
    """
    Check if the given APK file have methods to check for root.

    :param apk_file: Path to the image to be tested.
    """
    try:
        _, _, dex = analyze_apk(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    root_checker_methods = {
        'isRooted',
        'checkForDangerousProps',
        'checkForBusyBoxBinary',
        'checkForSuBinary',
        'checkSuExists',
    }

    if any(x.name in root_checker_methods for x in dex.get_methods()):
        show_close('App verifies for root', details=dict(apk=apk_file))
        return False
    show_open('App doesn\'t verify for root', details=dict(apk=apk_file))
    return True
