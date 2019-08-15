# -*- coding: utf-8 -*-

"""This module allows to check ``APK`` vulnerabilities."""

# standard imports
from functools import lru_cache

# 3rd party imports
from androguard.misc import AnalyzeAPK
from androguard.core.bytecodes.apk import APK

# local imports
from fluidasserts import show_open
from fluidasserts import show_close
from fluidasserts import show_unknown
from fluidasserts.utils.decorators import track, level, notify


@lru_cache(maxsize=None, typed=True)
def analyze_apk(path: str) -> tuple:
    """Return the resultant objects after analyzing the apk."""
    return AnalyzeAPK(path)


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


@notify
@level('medium')
@track
def uses_dangerous_perms(apk_file: str) -> bool:
    """
    Check if the given APK uses dangerous permissions.

    :param apk_file: Path to the image to be tested.
    """
    insecure_perms = {
        'android.permission.READ_CALENDAR',
        'android.permission.WRITE_CALENDAR',
        'android.permission.CAMERA',
        'android.permission.READ_CONTACTS',
        'android.permission.WRITE_CONTACTS',
        'android.permission.GET_ACCOUNTS',
        'android.permission.ACCESS_FINE_LOCATION',
        'android.permission.ACCESS_COARSE_LOCATION',
        'android.permission.RECORD_AUDIO',
        'android.permission.READ_PHONE_STATE',
        'android.permission.READ_PHONE_NUMBERS ',
        'android.permission.CALL_PHONE',
        'android.permission.ANSWER_PHONE_CALLS ',
        'android.permission.READ_CALL_LOG',
        'android.permission.WRITE_CALL_LOG',
        'android.permission.ADD_VOICEMAIL',
        'android.permission.USE_SIP',
        'android.permission.PROCESS_OUTGOING_CALLS',
        'android.permission.BODY_SENSORS',
        'android.permission.SEND_SMS',
        'android.permission.RECEIVE_SMS',
        'android.permission.READ_SMS',
        'android.permission.RECEIVE_WAP_PUSH',
        'android.permission.RECEIVE_MMS',
        'android.permission.READ_EXTERNAL_STORAGE',
        'android.permission.WRITE_EXTERNAL_STORAGE',
    }
    try:
        apk = APK(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    effective_dangerous = [x for x in apk.get_permissions()
                           if x in insecure_perms]
    if effective_dangerous:
        show_open('APK uses dangerous permissions',
                  details=dict(apk=apk_file, permissions=effective_dangerous))
        return True
    show_close('APK doesn\'t use dangerous permissions',
               details=dict(apk=apk_file))
    return False


@notify
@level('medium')
@track
def has_fragment_injection(apk_file: str) -> bool:
    """
    Check if the given APK is vulnerable to fragment injection.

    :param apk_file: Path to the image to be tested.
    """
    try:
        apk = APK(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    sdk_version = apk.get_target_sdk_version()
    target_sdk_version = int(sdk_version) if sdk_version else 0

    if target_sdk_version == 0:
        show_unknown('Could not determine target SDK version',
                     details=dict(apk=apk_file))
        return False
    if target_sdk_version < 19:
        show_open('APK vulnerable to fragment injection',
                  details=dict(apk=apk_file))
        return True
    show_close('APK not vulnerable to fragment injection',
               details=dict(apk=apk_file))
    return False
