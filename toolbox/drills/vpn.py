# Standard libraries
import os
import subprocess
from toolbox.utils import generic

# Local libraries
from toolbox import logger


def main(subs: str) -> bool:
    """Use subs vpn"""
    success: bool = True
    config_file = f'toolbox/vpns/{subs}'
    vpn_list = [f for f in os.listdir('toolbox/vpns/')
                if os.path.isfile(os.path.join('toolbox/vpns/', f))]

    if (os.path.exists(f'{config_file}-bogota.sh') and
            os.path.exists(f'{config_file}-medellin.sh')):
        city = input(('Do you want to use bogota\'s or medellin\'s'
                      ' VPN? [1: Bogota - 2: Medellin]: '))
        if city == '1':
            generic.aws_login(f'continuous-{subs}')
            subprocess.call(
                f'./{config_file}-bogota.sh',
                shell=True
            )
        else:
            generic.aws_login(f'continuous-{subs}')
            subprocess.call(
                f'./{config_file}-medellin.sh',
                shell=True
            )
    else:
        if not os.path.isfile(f'{config_file}.sh'):
            logger.error("No VPN file found")
            logger.info(f'Available VPNs:\n{vpn_list}')
            success = False
        else:
            generic.aws_login(f'continuous-{subs}')
            subprocess.call(
                f'./{config_file}.sh',
                shell=True
            )
    return success
