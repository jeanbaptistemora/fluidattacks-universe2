# Standard libraries
from toolbox.utils import generic

# Local libraries
from toolbox.logger import LOGGER
from toolbox.utils.function import shield, RetryAndFinallyReturn


@shield(retries=1)
def main() -> bool:
    """Use subs vpn"""
    vpn_status, _, _ = generic.run_command(
        cmd=['nmcli', 'connection', 'show', 'fluidvpn'],
        cwd='.',
        env={},
    )
    if vpn_status > 0:
        LOGGER.info('Setting up the vpn')
        psk = input("enter your psk: ")
        username = input("enter your username: ")
        vpn_data = (" gateway = 190.217.110.94,"
                    " ipsec-enabled = yes,"
                    f" ipsec-psk = {psk},"
                    " mru = 1400,"
                    " mtu = 1400,"
                    " password-flags = 0,"
                    " refuse-chap = yes,"
                    " refuse-eap = yes,"
                    " refuse-mschap = yes,"
                    " refuse-pap = yes,"
                    f" user = {username}")
        command = [
            'nmcli',
            'connection',
            'add',
            'connection.id',
            'fluidvpn',
            'con-name',
            'fluidvpn',
            'type',
            'VPN',
            'vpn-type',
            'l2tp',
            'ifname',
            '--',
            'connection.autoconnect',
            'no',
            'ipv4.method',
            'auto',
            'vpn.data',
            vpn_data,
        ]
        status, _, stderr = generic.run_command(
            cmd=command,
            cwd='.',
            env={},
        )
        if status > 0:
            LOGGER.error('Could not configure VPN')
            LOGGER.error(stderr)
            raise RetryAndFinallyReturn()

    command = ['nmcli', 'connection', 'up', 'fluidvpn']
    LOGGER.info('Connecting to the VPN')
    status, _, stderr = generic.run_command(
        cmd=command,
        cwd='.',
        env={},
    )
    if status > 0:
        LOGGER.error('Could not connect to the VPN')
        LOGGER.error(stderr)
        raise RetryAndFinallyReturn()

    return True
