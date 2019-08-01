# -*- coding: utf-8 -*-

"""This module allows to check ``APK`` vulnerabilities."""

# standard imports

# 3rd party imports
from androguard.core.bytecodes.apk import APK

# local imports
from fluidasserts import show_open
from fluidasserts import show_close
from fluidasserts import show_unknown
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
        apk = APK(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    if apk.is_signed():
        show_close('APK file is signed', details=dict(apk=apk_file))
        return False
    show_open('APK file is not signed', details=dict(apk=apk_file))
    return True
