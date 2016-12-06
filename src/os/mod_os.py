# -*- coding: utf-8 -*-
"""
Modulo OS general
"""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts.os import linux_generic
from fluidasserts.os import windows_server_2008_plus


def is_os_min_priv_disabled(server, username, password, ssh_config,
                            os_type):
    """
    Checks if umask or similar is secure
    """
    if os_type is 'LINUX_GENERIC':
        return \
            linux_generic.is_os_min_priv_disabled(server, username,
                                                  password,
                                                  ssh_config)
    elif os_type is 'WINDOWS_SERVER_2008_PLUS':
        return \
            windows_server_2008_plus.is_os_min_priv_disabled(server,
                                                             username,
                                                             password,
                                                             ssh_config)


def is_os_sudo_disabled(server, username, password, ssh_config, os_type):
    """
    Checks if there's sudo or similar installed
    """
    if os_type is 'LINUX_GENERIC':
        return \
            linux_generic.is_os_sudo_disabled(server, username,
                                              password,
                                              ssh_config)
    elif os_type is 'WINDOWS_SERVER_2008_PLUS':
        return \
            windows_server_2008_plus.is_os_sudo_disabled(server,
                                                         username,
                                                         password,
                                                         ssh_config)


def is_os_compilers_installed(server, username, password, ssh_config,
                              os_type):
    """
    Checks if there's any compiler installed
    """
    if os_type is 'LINUX_GENERIC':
        return \
            linux_generic.is_os_compilers_installed(server, username,
                                                    password,
                                                    ssh_config)
    elif os_type is 'WINDOWS_SERVER_2008_PLUS':
        return \
            windows_server_2008_plus.is_os_compilers_installed(server,
                                                               username,
                                                               password,
                                                               ssh_config)


def is_os_antimalware_not_installed(server, username, password, ssh_config,
                                    os_type):
    """
    Checks if there's any antimalware installed
    """
    if os_type is 'LINUX_GENERIC':
        return \
            linux_generic.is_os_antimalware_not_installed(server,
                                                          username,
                                                          password,
                                                          ssh_config)
    elif os_type is 'WINDOWS_SERVER_2008_PLUS':
        return \
            windows_server_2008_plus.is_os_antimalware_not_installed(server,
                                                                     username,
                                                                     password,
                                                                     ssh_config)


def is_os_remote_admin_enabled(server, username, password, ssh_config,
                               os_type):
    """
    Checks if admins can remotely login
    """
    if os_type is 'LINUX_GENERIC':
        return \
            linux_generic.is_os_remote_admin_enabled(server,
                                                     username,
                                                     password,
                                                     ssh_config)
    elif os_type is 'WINDOWS_SERVER_2008_PLUS':
        return \
            windows_server_2008_plus.is_os_remote_admin_enabled(server,
                                                                username,
                                                                password,
                                                                ssh_config)


def is_os_syncookies_disabled(server, username, password, ssh_config,
                              os_type):
    """
    Checks if SynCookies or similar is enabled
    """
    if os_type is 'LINUX_GENERIC':
        return \
            linux_generic.is_os_syncookies_disabled(server,
                                                    username,
                                                    password,
                                                    ssh_config)
    elif os_type is 'WINDOWS_SERVER_2008_PLUS':
        return \
            windows_server_2008_plus.is_os_syncookies_disabled(server,
                                                               username,
                                                               password,
                                                               ssh_config)
