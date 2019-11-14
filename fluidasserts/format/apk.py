# -*- coding: utf-8 -*-

"""This module allows to check ``APK`` vulnerabilities."""

# standard imports
import re
from typing import Any, List, Tuple
from functools import lru_cache
import logging

# 3rd party imports
from androguard.misc import AnalyzeAPK
from androguard.core.analysis import analysis
from androguard.core.bytecodes import apk, dvm
import androguard

# local imports
from fluidasserts import SAST, LOW, MEDIUM, HIGH, _get_result_as_tuple_sast
from fluidasserts.utils.decorators import api, unknown_if

# Set androguard logging levels to CRITICAL
androguard.core.androconf.show_logging(level=logging.CRITICAL)


@lru_cache(maxsize=None, typed=True)
def analyze_apk(path: str) -> tuple:
    """Return the resultant objects after analyzing the apk."""
    return AnalyzeAPK(path)


@lru_cache(maxsize=None, typed=True)
def get_dex(path: str) -> tuple:
    """Return DEX analysis from APK file."""
    apk_obj = apk.APK(path)
    _dex = dvm.DalvikVMFormat(apk_obj.get_dex())
    dex = analysis.Analysis()
    dex.add(_dex)
    dex.create_xref()
    return dex


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

    if not met_ana:
        return None

    used_by = [x.name for x, _, _ in met_ana.get_xref_from()
               if 'Activity' in x.name]

    return used_by


def get_http_urls(dex):
    """Get HTTP URLs used in APK file."""
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


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def is_unsigned(apk_file: str) -> tuple:
    """
    Check if the given APK file is signed.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK is unsigned.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj = apk.APK(apk_file)

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='APK file is not signed',
        msg_closed='APK file is signed',
        open_if=not apk_obj.is_signed())


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def not_checks_for_root(apk_file: str) -> tuple:
    """
    Check if the given APK file have methods to check for root.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK has means for checking if the device is rooted.
                currently the methods to check for root are *isRooted*,
                *checkForDangerousProps*, *checkForBusyBoxBinary*,
                *checkForSuBinary*, and *checkSuExists*.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    _, _, dex = analyze_apk(apk_file)

    root_checker_methods = {
        'isRooted',
        'checkForDangerousProps',
        'checkForBusyBoxBinary',
        'checkForSuBinary',
        'checkSuExists',
    }

    check_root = any(x.name in root_checker_methods for x in dex.get_methods())

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='App does not verify for root',
        msg_closed='App verifies for root',
        open_if=not check_root)


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def uses_dangerous_perms(apk_file: str) -> tuple:
    """
    Check if the given APK uses dangerous permissions.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK uses dangerous permissions.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj = apk.APK(apk_file)

    dangerous = {
        'dangerous'
    }

    perms = apk_obj.get_details_permissions()

    effective_dangerous: List[Tuple[str, Any]] = [(x, perms[x][1])
                                                  for x in perms
                                                  if perms[x][0] in dangerous]

    has_effective_dangerous: bool = bool(effective_dangerous)

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open=f'APK uses dangerous permissions',
        msg_closed='APK does not use dangerous permissions',
        open_if=has_effective_dangerous,
        fingerprint={'Dangerous permissions': effective_dangerous})


@api(risk=MEDIUM, kind=SAST)
@unknown_if(AssertionError, FileNotFoundError, apk.Error, dvm.Error)
def has_fragment_injection(apk_file: str) -> tuple:
    """
    Check if the given APK is vulnerable to fragment injection.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if the target SDK version is less than 19, and
                *PreferenceActivity* is present.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj, dvms, _ = analyze_apk(apk_file)

    sdk_version = apk_obj.get_target_sdk_version()
    target_sdk_version = int(sdk_version) if sdk_version else 0

    if target_sdk_version == 0:
        raise AssertionError('Could not determine target SDK version')

    is_vulnerable: bool = target_sdk_version < 19 \
        and 'PreferenceActivity' in get_activities_source(dvms)

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='APK vulnerable to fragment injection',
        msg_closed='APK not vulnerable to fragment injection',
        open_if=is_vulnerable)


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def webview_caches_javascript(apk_file: str) -> tuple:
    """
    Check if the given APK has WebView that caches JavaScript data and code.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK has WebView that caches JavaScript.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    _, dvms, _ = analyze_apk(apk_file)
    act_source = get_activities_source(dvms)

    is_vulnerable: bool = 'setJavaScriptEnabled' in act_source \
        and 'clearCache' not in act_source

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='WebView does not clear JavaScript cache',
        msg_closed='WebView has JavaScript not enabled or clears cache',
        open_if=is_vulnerable)


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def webview_allows_resource_access(apk_file: str) -> tuple:
    """
    Check if the given APK has WebView that allows resource access.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK has *setAllowContentAccess*,
                *setAllowFileAccess*, *setAllowFileAccessFromFileURLs*,
                *setAllowUniversalAccessFromFileURLs* activities.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    dangerous_allows = {
        'setAllowContentAccess',
        'setAllowFileAccess',
        'setAllowFileAccessFromFileURLs',
        'setAllowUniversalAccessFromFileURLs',
    }

    _, dvms, _ = analyze_apk(apk_file)
    act_source = get_activities_source(dvms)

    effective_dangerous: List[str] = []
    if 'setJavaScriptEnabled' in act_source:
        effective_dangerous = list(filter(
            act_source.__contains__, dangerous_allows))

    has_dangerous_permissions: bool = bool(effective_dangerous)

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open=f'WebView allows resource access',
        msg_closed='WebView does not allow resource access',
        open_if=has_dangerous_permissions,
        fingerprint={'Dangerous permissions': effective_dangerous})


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def not_forces_updates(apk_file: str) -> tuple:
    """
    Check if the given APK forces to use the latest version.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if *AppUpdateManager* is not in activities source.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    _, dvms, _ = analyze_apk(apk_file)
    act_source = get_activities_source(dvms)

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='APK not forces updating',
        msg_closed='APK forces updating',
        open_if='AppUpdateManager' not in act_source)


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def not_verifies_ssl_hostname(apk_file: str) -> tuple:
    """
    Check if the given APK doesn't verify the SSLSocket hostname.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK does not have *getDefaultHostnameVerifier* in
                activities source.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    _, dvms, _ = analyze_apk(apk_file)
    act_source = get_activities_source(dvms)

    is_vulnerable: bool = False

    msg_closed: str = 'APK does not use SSLSocket'

    if 'SSLSocket' in act_source:
        if 'getDefaultHostnameVerifier' in act_source:
            msg_closed = 'APK verifies hostname in SSL cert'
        else:
            is_vulnerable = True

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='APK does not verify hostname in SSL cert',
        msg_closed=msg_closed,
        open_if=is_vulnerable)


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def not_pinned_certs(apk_file: str) -> tuple:
    """
    Check if the given APK does not pin x509 certificates.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if *res/xml/network_security_config.xml* is not
                present in APK or *pin-set* is not in the
                *network_security_config/xml* file.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj = apk.APK(apk_file)

    is_vulnerable: bool = True

    msg_open = 'APK does not pin certificates'

    try:
        net_conf = str(apk_obj.get_file('res/xml/network_security_config.xml'))
    except androguard.core.bytecodes.apk.FileNotPresent:
        msg_open = 'No declarative pinning file was found'
    else:
        if 'pin-set' in net_conf:
            is_vulnerable = False

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open=msg_open,
        msg_closed='APK pines certificates',
        open_if=is_vulnerable)


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def allows_user_ca(apk_file: str) -> tuple:
    """
    Check if the given APK allows to trust on user-given CAs.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK allows to trust on user-given CAs.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj = apk.APK(apk_file)

    msg_open = ''
    msg_closed = ''
    try:
        net_conf = str(apk_obj.get_file('res/xml/network_security_config.xml'))
    except androguard.core.bytecodes.apk.FileNotPresent:
        sdk_version = apk_obj.get_target_sdk_version()
        target_sdk = int(sdk_version) if sdk_version else 0
        if target_sdk < 24:
            msg_open = 'No network security config file found and SDK version \
allows user-supplied CAs by default'
            return _get_result_as_tuple_sast(
                path=apk_file,
                msg_open=msg_open,
                msg_closed=msg_closed,
                open_if=True
            )
        msg_closed = 'No network security config file found but SDK version \
defaults to deny user-supplied CAs'
        return _get_result_as_tuple_sast(
            path=apk_file,
            msg_open=msg_open,
            msg_closed=msg_closed,
            open_if=False
        )

    result = False
    if 'trust-anchors' in net_conf and 'user' in net_conf:
        msg_open = 'APK allows to trust user-supplied CAs'
        result = True
    else:
        msg_closed = 'APK denies to trust user-supplied CAs'
    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open=msg_open,
        msg_closed=msg_closed,
        open_if=result
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def has_debug_enabled(apk_file: str) -> tuple:
    """
    Check if the given APK has debug enabled.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK has debug enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj = apk.APK(apk_file)

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='APK has debug enabled',
        msg_closed='APK has debug disabled',
        open_if=apk_obj.get_element("application", "debuggable") == 'true'
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def not_obfuscated(apk_file: str) -> tuple:
    """
    Check if the given APK is not obfuscated.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK is not obfuscated.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    _, dvms, _ = analyze_apk(apk_file)

    not_obfs_dvms = [dvm.header.signature.hex()
                     for dvm in dvms
                     if not analysis.is_ascii_obfuscation(dvm)]

    has_not_obfs_dvms: bool = bool(not_obfs_dvms)

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open=f'APK has DVMs not obfuscated',
        msg_closed='All APK DVMs are obfuscated',
        open_if=has_not_obfs_dvms,
        fingerprint={'DVMs without obfuscation': not_obfs_dvms})


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def uses_insecure_delete(apk_file: str) -> tuple:
    """
    Check if the given APK uses insecure delete of data.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK uses insecure delete of data
                (*Ljava/io/File;->delete()Z*).
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    dex = get_dex(apk_file)

    deletes_insecure = is_method_present(
        dex, 'Ljava/io/File;', 'delete', '()Z')

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='APK does not securely remove files',
        msg_closed='APK securely remove files',
        open_if=deletes_insecure)


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def uses_http_resources(apk_file: str) -> tuple:
    """
    Check if the given APK references HTTP (not HTTPS) resources.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK references HTTP (not HTTPS) resources.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    dex = get_dex(apk_file)

    insecure_urls = get_http_urls(dex)

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open=f'APK references non HTTPS URLs',
        msg_closed='All HTTP references in APK use HTTPS',
        open_if=insecure_urls,
        fingerprint=insecure_urls)


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def socket_uses_getinsecure(apk_file: str) -> tuple:
    """
    Check if the given APK uses sockets created with getInsecure.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK uses *getInsecure* method from the
                *android.net.SSLCertificateSocketFactory* class.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    dex = get_dex(apk_file)

    uses_get_insecure = is_method_present(
        dex=dex,
        class_name='Landroid/net/SSLCertificateSocketFactory;',
        method='getInsecure',
        descriptor=('(I Landroid/net/SSLSessionCache;)'
                    'Ljavax/net/ssl/SSLSocketFactory;'))

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='APK uses sockets created with getInsecure',
        msg_closed='APK does not use sockets created with getInsecure',
        open_if=uses_get_insecure)


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def allows_backup(apk_file: str) -> tuple:
    """
    Check if the given APK allows ADB backups.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK have the **allowBackup** attribute not set to
                false.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj = apk.APK(apk_file)

    does_allow_backup: bool = \
        apk_obj.get_attribute_value('application', 'allowBackup') != 'false'

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='APK allows ADB backups',
        msg_closed='APK does not allow ADB backups',
        open_if=does_allow_backup)


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def is_exported(apk_file: str) -> tuple:
    """
    Check if the given APK exports data to other installed apps.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK have the **exported** attribute set to
                **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj = apk.APK(apk_file)

    is_data_exported: bool = \
        apk_obj.get_attribute_value('provider', 'exported') == 'true'

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='App data is being exported to other apps in device',
        msg_closed='App data is not being exported to other apps in device',
        open_if=is_data_exported)


@api(risk=HIGH, kind=SAST)
@unknown_if(FileNotFoundError, apk.Error, dvm.Error)
def has_frida(apk_file: str) -> tuple:
    """
    Check if the given APK has **Frida** gadget embedded.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK have the **Frida** gadget in its files.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj = apk.APK(apk_file)

    frida_gadgets: List[str] = [x for x in apk_obj.get_files() if 'frida' in x]
    is_frida_gadget_in_files: bool = bool(frida_gadgets)

    return _get_result_as_tuple_sast(
        path=apk_file,
        msg_open='APK has Frida gadget embedded',
        msg_closed='APK does not have Frida gadget embedded',
        open_if=is_frida_gadget_in_files,
        fingerprint={'frida_gadgets': frida_gadgets})
