# Standard libraries
import os
import subprocess
from toolbox.utils import generic

# Local libraries
from toolbox.logger import LOGGER
from toolbox.utils.function import shield, RetryAndFinallyReturn


@shield(retries=1)
def main(subs: str) -> bool:
    """Use subs vpn"""
    success: bool = True
    config_file = f'tools/vpns/{subs}'
    vpn_list = [f for f in os.listdir('tools/vpns')
                if os.path.isfile(os.path.join('tools/vpns/', f))]

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
            LOGGER.error("No VPN file found")
            LOGGER.info('Available VPNs:\n%s', vpn_list)
            success = False
        else:
            generic.aws_login(f'continuous-{subs}')
            subprocess.call(
                f'./{config_file}.sh',
                shell=True
            )

    if not success:
        raise RetryAndFinallyReturn()
    return success
