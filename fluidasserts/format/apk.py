# -*- coding: utf-8 -*-

"""This module allows to check ``APK`` vulnerabilities."""

# standard imports
from functools import lru_cache
import logging
from typing import List

# 3rd party imports
from androguard.misc import AnalyzeAPK
from androguard.core.analysis import analysis
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
import androguard

# local imports
from fluidasserts import Unit, LOW, MEDIUM, SAST, OPEN, CLOSED, UNKNOWN
from fluidasserts import show_open
from fluidasserts import show_close
from fluidasserts import show_unknown
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.utils.decorators import track, level, notify

androguard.core.androconf.show_logging(level=logging.CRITICAL)


@lru_cache(maxsize=None, typed=True)
def analyze_apk(path: str) -> tuple:
    """Return the resultant objects after analyzing the apk."""
    return AnalyzeAPK(path)


@lru_cache(maxsize=None, typed=True)
def get_dex(path: str) -> tuple:
    """Return DEX analysis from APK file."""
    apk_obj = APK(path)
    _dex = DalvikVMFormat(apk_obj.get_dex())
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


def _get_result_as_tuple(*,
                         apk_file: str,
                         msg_open: str, msg_closed: str,
                         open_if: bool) -> tuple:
    """Return the tuple version of the Result object."""
    units: List[Unit] = [
        Unit(where=f'{apk_file}',
             specific=[msg_open if open_if else msg_closed])]

    if open_if:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def is_unsigned(apk_file: str) -> tuple:
    """
    Check if the given APK file is signed.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK is unsigned.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk = APK(apk_file)

    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open='APK file is not signed',
        msg_closed='APK file is signed',
        open_if=not apk.is_signed()
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def not_checks_for_root(apk_file: str) -> tuple:
    """
    Check if the given APK file have methods to check for root.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK has means for checking if the device is rooted.
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
    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open='App doesn\'t verify for root',
        msg_closed='App verifies for root',
        open_if=not check_root
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def uses_dangerous_perms(apk_file: str) -> tuple:
    """
    Check if the given APK uses dangerous permissions.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK uses dangerous permissions.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk = APK(apk_file)

    dangerous = {
        'dangerous'
    }

    perms = apk.get_details_permissions()
    effective_dangerous = [(x, perms[x][1]) for x in perms
                           if perms[x][0] in dangerous]

    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open=f'APK uses dangerous permissions: {effective_dangerous}',
        msg_closed='APK doesn\'t use dangerous permissions',
        open_if=effective_dangerous
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_fragment_injection(apk_file: str) -> tuple:
    """
    Check if the given APK is vulnerable to fragment injection.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK is vulnerable to fragment injection.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj, dvms, _ = analyze_apk(apk_file)

    sdk_version = apk_obj.get_target_sdk_version()
    target_sdk_version = int(sdk_version) if sdk_version else 0

    if target_sdk_version == 0:
        return UNKNOWN, f'Could not determine target SDK version on {apk_file}'

    is_vuln = False
    if target_sdk_version < 19:
        act_source = get_activities_source(dvms)
        if 'PreferenceActivity' in act_source:
            is_vuln = True
    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open='APK vulnerable to fragment injection',
        msg_closed='APK not vulnerable to fragment injection',
        open_if=is_vuln
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
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

    is_vuln = False
    if 'setJavaScriptEnabled' in act_source:
        if 'clearCache' not in act_source:
            is_vuln = True
    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open='WebView not clears JavaScript cache',
        msg_closed='WebView has JavaScript not enabled or clears cache',
        open_if=is_vuln
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def webview_allows_resource_access(apk_file: str) -> bool:
    """
    Check if the given APK has WebView that allows resource access.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK has WebView that allows resource access.
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

    effective_dangerous = []
    if 'setJavaScriptEnabled' in act_source:
        effective_dangerous = [x for x in dangerous_allows
                               if x in act_source]
    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open=f'WebView allows resource access: {effective_dangerous}',
        msg_closed='WebView does not allow resource access',
        open_if=effective_dangerous
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def not_forces_updates(apk_file: str) -> tuple:
    """
    Check if the given APK forces to use the latest version.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK forces to use the latest version.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    _, dvms, _ = analyze_apk(apk_file)
    act_source = get_activities_source(dvms)
    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open='APK not forces updating',
        msg_closed='APK forces updating',
        open_if='AppUpdateManager' not in act_source
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def not_verifies_ssl_hostname(apk_file: str) -> tuple:
    """
    Check if the given APK doesn't verify the SSLSocket hostname.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK doesn't verify the SSLSocket hostname.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    _, dvms, _ = analyze_apk(apk_file)
    act_source = get_activities_source(dvms)

    result = False
    msg_closed = ''
    if 'SSLSocket' in act_source:
        if 'getDefaultHostnameVerifier' not in act_source:
            show_open('APK does not verify hostname in SSL cert',
                      details=dict(apk=apk_file))
            result = True
        else:
            msg_closed = 'APK verifies hostname in SSL cert'
    else:
        msg_closed = 'APK does not use SSLSocket'
    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open='APK does not verify hostname in SSL cert',
        msg_closed=msg_closed,
        open_if=result
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def not_pinned_certs(apk_file: str) -> tuple:
    """
    Check if the given APK does not pin x509 certificates.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK does not pin x509 certificates.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj = APK(apk_file)

    is_vuln = False
    msg_open = ''
    try:
        net_conf = str(apk_obj.get_file('res/xml/network_security_config.xml'))
    except androguard.core.bytecodes.apk.FileNotPresent:
        msg_open = 'No declarative pinning file was found'
        is_vuln = True
    else:
        if 'pin-set' not in net_conf:
            msg_open = 'APK does not pin certificates'
            is_vuln = True
        else:
            is_vuln = False
    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open=msg_open,
        msg_closed='APK pines certificates',
        open_if=is_vuln
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def allows_user_ca(apk_file: str) -> tuple:
    """
    Check if the given APK allows to trust on user-given CAs.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK allows to trust on user-given CAs.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj = APK(apk_file)

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
            return _get_result_as_tuple(
                apk_file=apk_file,
                msg_open=msg_open,
                msg_closed=msg_closed,
                open_if=True
            )
        msg_closed = 'No network security config file found but SDK version \
defaults to deny user-supplied CAs'
        return _get_result_as_tuple(
            apk_file=apk_file,
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
    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open=msg_open,
        msg_closed=msg_closed,
        open_if=result
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_debug_enabled(apk_file: str) -> tuple:
    """
    Check if the given APK has debug enabled.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK has debug enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    apk_obj = APK(apk_file)

    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open='APK has debug enabled',
        msg_closed='APK has debug disabled',
        open_if=apk_obj.get_element("application", "debuggable") == 'true'
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
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
    not_obfs = [dvm.header.signature.hex() for dvm in dvms
                if not analysis.is_ascii_obfuscation(dvm)]
    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open=f'APK has DVMs not obfuscated: {not_obfs}',
        msg_closed='All APK DVMs are obfuscated',
        open_if=not_obfs
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def uses_insecure_delete(apk_file: str) -> tuple:
    """
    Check if the given APK uses insecure delete of data.

    :param apk_file: Path to the image to be tested.
    :returns: - ``OPEN`` if APK uses insecure delete of data.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    dex = get_dex(apk_file)

    deletes_insecure = is_method_present(dex, 'Ljava/io/File;', 'delete',
                                         '()Z')

    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open='APK does not securely remove files',
        msg_closed='APK securely remove files',
        open_if=deletes_insecure
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
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

    return _get_result_as_tuple(
        apk_file=apk_file,
        msg_open=f'APK references insecure URLs: {insecure_urls}',
        msg_closed='All HTTP references in APK use HTTPS',
        open_if=insecure_urls
    )


@notify
@level('low')
@track
def socket_uses_getinsecure(apk_file: str) -> bool:
    """
    Check if the given APK uses sockets created with getInsecure.

    :param apk_file: Path to the image to be tested.
    """
    try:
        dex = get_dex(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    class_name = 'Landroid/net/SSLCertificateSocketFactory;'
    method_name = 'getInsecure'
    desc = '(I Landroid/net/SSLSessionCache;)Ljavax/net/ssl/SSLSocketFactory;'

    uses = is_method_present(dex, class_name, method_name, desc)

    if uses:
        show_open('APK uses sockets created with getInsecure',
                  details=dict(apk=apk_file,
                               get_insecure_uses=uses))
        return True
    show_close('APK doesn\'t use sockets created with getInsecure',
               details=dict(apk=apk_file))
    return False


@notify
@level('low')
@track
def allows_backup(apk_file: str) -> bool:
    """
    Check if the given APK allows ADB backups.

    :param apk_file: Path to the image to be tested.
    """
    try:
        apk_obj = APK(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    if apk_obj.get_attribute_value('application', 'allowBackup') != 'false':
        show_open('APK allows ADB backups',
                  details=dict(apk=apk_file))
        return True
    show_close('APK disallows ADB backups',
               details=dict(apk=apk_file))
    return False


@notify
@level('medium')
@track
def is_exported(apk_file: str) -> bool:
    """
    Check if the given APK exports data to other installed apps.

    :param apk_file: Path to the image to be tested.
    """
    try:
        apk_obj = APK(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    exported = apk_obj.get_attribute_value('provider', 'exported')

    if exported == 'true':
        show_open('App data is exported to other apps in device',
                  details=dict(apk=apk_file))
        return True
    show_close('App data is not exported to other apps in device',
               details=dict(apk=apk_file))
    return False


@notify
@level('high')
@track
def has_frida(apk_file: str) -> bool:
    """
    Check if the given APK has Frida gadget embedded.

    :param apk_file: Path to the image to be tested.
    """
    try:
        apk_obj = APK(apk_file)
    except FileNotFoundError as exc:
        show_unknown('Error reading file',
                     details=dict(apk=apk_file, error=str(exc)))
        return False

    frida = [x for x in apk_obj.get_files() if 'frida' in x]

    if frida:
        show_open('APK has frida gadget embedded',
                  details=dict(apk=apk_file))
        return True
    show_close('APK doesn\' have frida gadget embedded',
               details=dict(apk=apk_file))
    return False
