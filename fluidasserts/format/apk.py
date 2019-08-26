# -*- coding: utf-8 -*-

"""This module allows to check ``APK`` vulnerabilities."""

# standard imports
from functools import lru_cache
import logging

# 3rd party imports
from androguard.misc import AnalyzeAPK
from androguard.core.bytecodes.apk import APK
import androguard

# local imports
from fluidasserts import show_open
from fluidasserts import show_close
from fluidasserts import show_unknown
from fluidasserts.utils.decorators import track, level, notify

androguard.core.androconf.show_logging(level=logging.CRITICAL)


@lru_cache(maxsize=None, typed=True)
def analyze_apk(path: str) -> tuple:
    """Return the resultant objects after analyzing the apk."""
    return AnalyzeAPK(path)


def get_activities_source(dvms: list) -> str:
    """Decompile given Dalvik VM images."""
    source = [x.get_source() for dvm in dvms for x in dvm.get_classes()
              if 'Activity' in x.name]
    return "".join(source)


def is_method_present(dex, class_name, method, descriptor):
    """Search if method is present in decompiled code."""
    met_ana = dex.get_method_analysis_by_name(class_name=class_name,
                                              method_name=method,
                                              method_descriptor=descriptor)

    used_by = [x.name for x, _, _ in met_ana.get_xref_from()
               if 'Activity' in x.name]

    return used_by


def get_http_urls(dex):
    """Get HTTP URLs used in APK file."""
    import re

    whitelist = {
        'http://schemas.android.com/',
        'http://www.w3.org/',
        'http://apache.org/',
        'http://xml.org/',
        'http://localhost/',
        'http://127.0.0.1/',
        'http://java.sun.com/'
    }
    return [x.get_value() for x in dex.get_strings()
            if re.match(r'^http?\:\/\/.+', x.get_value()) and
            not any(re.match(whitel, x.get_value()) for whitel in whitelist)]


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
        apk, dvms, _ = analyze_apk(apk_file)
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
        act_source = get_activities_source(dvms)
        if 'PreferenceActivity' in act_source:
            show_open('APK vulnerable to fragment injection',
                      details=dict(apk=apk_file))
            return True
    show_close('APK not vulnerable to fragment injection',
               details=dict(apk=apk_file))
    return False


@notify
@level('low')
@track
def webview_caches_javascript(apk_file: str) -> bool:
    """
    Check if the given APK has WebView that caches JavaScript data and code.

    :param apk_file: Path to the image to be tested.
    """
    try:
        apk, dvms, _ = analyze_apk(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    act_source = get_activities_source(dvms)

    if 'setJavaScriptEnabled' in act_source:
        if 'clearCache' not in act_source:
            show_open('WebView has JavaScript enabled \
but doesn\'t clear cache',
                      details=dict(apk=apk_file))
            return True
    show_close('WebView has JavaScript not enabled or clears cache',
               details=dict(apk=apk_file))
    return False


@notify
@level('low')
@track
def webview_allows_resource_access(apk_file: str) -> bool:
    """
    Check if the given APK has WebView that allows resource access.

    :param apk_file: Path to the image to be tested.
    """
    dangerous_allows = {
        'setAllowContentAccess',
        'setAllowFileAccess',
        'setAllowFileAccessFromFileURLs',
        'setAllowUniversalAccessFromFileURLs',
    }
    try:
        apk, dvms, _ = analyze_apk(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    act_source = get_activities_source(dvms)

    if 'setJavaScriptEnabled' in act_source:
        effective_dangerous = [x for x in dangerous_allows
                               if x in act_source]
        if effective_dangerous:
            show_open('WebView allows resource access',
                      details=dict(apk=apk_file,
                                   dangerous_allows=effective_dangerous))
            return True
    show_close('WebView does not allow resource access',
               details=dict(apk=apk_file))
    return False


@notify
@level('low')
@track
def not_forces_updates(apk_file: str) -> bool:
    """
    Check if the given APK forces to use the latest version.

    :param apk_file: Path to the image to be tested.
    """
    try:
        apk, dvms, _ = analyze_apk(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    act_source = get_activities_source(dvms)

    if 'AppUpdateManager' not in act_source:
        show_open('APK not forces updating', details=dict(apk=apk_file))
        return True
    show_close('APK forces updating',
               details=dict(apk=apk_file))
    return False


@notify
@level('low')
@track
def not_verifies_ssl_hostname(apk_file: str) -> bool:
    """
    Check if the given APK doesn't verify the SSLSocket hostname.

    :param apk_file: Path to the image to be tested.
    """
    try:
        _, dvms, _ = analyze_apk(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    act_source = get_activities_source(dvms)

    result = False
    if 'SSLSocket' in act_source:
        if 'getDefaultHostnameVerifier' not in act_source:
            show_open('APK does not verify hostname in SSL cert',
                      details=dict(apk=apk_file))
            result = True
        else:
            show_close('APK verifies hostname in SSL cert',
                       details=dict(apk=apk_file))
    else:
        show_close('APK does not use SSLSocket',
                   details=dict(apk=apk_file))
    return result


@notify
@level('medium')
@track
def not_pinned_certs(apk_file: str) -> bool:
    """
    Check if the given APK does not pin x509 certificates.

    :param apk_file: Path to the image to be tested.
    """
    try:
        apk_obj = APK(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    try:
        net_conf = str(apk_obj.get_file('res/xml/network_security_config.xml'))
    except androguard.core.bytecodes.apk.FileNotPresent:
        show_open('No declarative pinning file was found',
                  details=dict(apk=apk_file))
        return True

    result = False
    if 'pin-set' not in net_conf:
        show_open('APK does not pin certificates',
                  details=dict(apk=apk_file))
        result = True
    else:
        show_close('APK pinnes certificates',
                   details=dict(apk=apk_file))
    return result


@notify
@level('low')
@track
def allows_user_ca(apk_file: str) -> bool:
    """
    Check if the given APK allows to trust on user-given CAs.

    :param apk_file: Path to the image to be tested.
    """
    try:
        apk_obj = APK(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    result = False
    try:
        net_conf = str(apk_obj.get_file('res/xml/network_security_config.xml'))
    except androguard.core.bytecodes.apk.FileNotPresent:
        target_sdk = int(apk_obj.get_target_sdk_version())
        if target_sdk < 24:
            show_open('No network security config file found and SDK version \
allows user-supplied CAs by default',
                      details=dict(apk=apk_file, target_sdk=target_sdk))
            result = True
        else:
            show_close('No network security config file found but SDK version \
defaults to deny user-supplied CAs',
                       details=dict(apk=apk_file, target_sdk=target_sdk))
            result = False
        return result

    result = False

    if 'trust-anchors' in net_conf and 'user' in net_conf:
        show_open('APK allows to trust user-supplied CAs',
                  details=dict(apk=apk_file))
        result = True
    else:
        show_close('APK denies to trust user-supplied CAs',
                   details=dict(apk=apk_file))
    return result


@notify
@level('low')
@track
def has_debug_enabled(apk_file: str) -> bool:
    """
    Check if the given APK has debug enabled.

    :param apk_file: Path to the image to be tested.
    """
    try:
        apk_obj = APK(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    if apk_obj.get_element("application", "debuggable") == 'true':
        show_open('APK has debug enabled', details=dict(apk=apk_file))
        return True
    show_close('APK has debug disabled', details=dict(apk=apk_file))
    return False


@notify
@level('low')
@track
def not_obfuscated(apk_file: str) -> bool:
    """
    Check if the given APK is not obfuscated.

    :param apk_file: Path to the image to be tested.
    """
    try:
        _, dvms, _ = analyze_apk(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    from androguard.core.analysis import analysis

    not_obfuscated = [dvm.header.signature.hex() for dvm in dvms
                      if not analysis.is_ascii_obfuscation(dvm)]

    if not_obfuscated:
        show_open('APK has DVMs not obfuscated',
                  details=dict(apk=apk_file, not_obfuscated=not_obfuscated))
        return True
    show_close('All APK DVMs are obfuscated', details=dict(apk=apk_file))
    return False


@notify
@level('low')
@track
def uses_insecure_delete(apk_file: str) -> bool:
    """
    Check if the given APK uses insecure delete of data.

    :param apk_file: Path to the image to be tested.
    """
    try:
        _, _, dex = analyze_apk(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    deletes_insecure = is_method_present(dex, 'Ljava/io/File;', 'delete',
                                         '()Z')

    if deletes_insecure:
        show_open('APK does not securely remove files',
                  details=dict(apk=apk_file,
                               deletes_insecure=deletes_insecure))
        return True
    show_close('APK securely remove files', details=dict(apk=apk_file))
    return False


@notify
@level('low')
@track
def uses_http_resources(apk_file: str) -> bool:
    """
    Check if the given APK references HTTP (not HTTPS) resources.

    :param apk_file: Path to the image to be tested.
    """
    try:
        _, _, dex = analyze_apk(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    insecure_urls = get_http_urls(dex)

    if insecure_urls:
        show_open('APK references insecure URLs',
                  details=dict(apk=apk_file,
                               insecure_urls=insecure_urls))
        return True
    show_close('All HTTP references in APK use HTTPS.',
               details=dict(apk=apk_file))
    return False
