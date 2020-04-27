# Standard library
import glob
import os
import sys

# Third party imports
import ruamel.yaml as yaml

# Local imports
from toolbox import (
    logger,
    utils,
)


def encrypt(subs: str) -> bool:
    """Encrypt a secrets.yml file for a subscription."""
    # pylint: disable=import-outside-toplevel
    from fluidasserts.helper import crypto

    utils.generic.aws_login(f'continuous-{subs}')

    for resources_path in glob.glob(
            f'subscriptions/{subs}/forces/*/resources'):
        plaintext_path: str = f'{resources_path}/plaintext.yml'
        encrypted_path: str = f'{resources_path}/secrets.yml'

        logger.info(
            f'Moving secrets from {plaintext_path} to {encrypted_path}')

        with open(plaintext_path) as plaintext_handle, \
                open(encrypted_path, 'w') as encrypted_handle:
            crypto.create_encrypted_yaml(
                key_b64=utils.generic.get_sops_secret(
                    f'forces_aws_secret_access_key',
                    f'subscriptions/{subs}/config/secrets.yaml',
                    f'continuous-{subs}'),
                secrets={
                    str(key): str(value)
                    for key, value in yaml.safe_load(
                        plaintext_handle.read())['secrets'].items()
                },
                file=encrypted_handle)

        logger.info('  Done!')
    return True


def decrypt(subs: str) -> bool:
    """Decrypt a secrets.yml file for a subscription."""
    # pylint: disable=import-outside-toplevel
    from fluidasserts.helper import crypto

    utils.generic.aws_login(f'continuous-{subs}')

    for resources_path in glob.glob(
            f'subscriptions/{subs}/forces/*/resources'):
        plaintext_path: str = f'{resources_path}/plaintext.yml'
        encrypted_path: str = f'{resources_path}/secrets.yml'

        logger.info(
            f'Moving secrets from {encrypted_path} to {plaintext_path}')

        if not os.path.exists(encrypted_path):
            logger.error(
                f'  No secrets.yml file found for {subs}')
            logger.error(
                f'    1. run $ fluid forces --init-secrets {subs}')
            logger.error(
                f'    2. put your secrets in {plaintext_path}')
            logger.error(
                f'    3. run $ fluid forces --encrypt {subs} ')
            sys.exit(78)
        else:
            crypto.create_decrypted_yaml(
                key_b64=utils.generic.get_sops_secret(
                    f'forces_aws_secret_access_key',
                    f'subscriptions/{subs}/config/secrets.yaml',
                    f'continuous-{subs}'),
                input_file=encrypted_path,
                output_file=plaintext_path)

            logger.info('  Done!')
    return True


def init(subs: str) -> bool:
    """Encrypt a secrets.yml file for a subscription."""
    for resources_path in (
            f'subscriptions/{subs}/forces/static/resources',
            f'subscriptions/{subs}/forces/dynamic/resources'):
        os.makedirs(resources_path, exist_ok=True)
        plaintext_path: str = f'{resources_path}/plaintext.yml'

        logger.info(f'Initializing {plaintext_path}')
        if not os.path.exists(plaintext_path):
            with open(plaintext_path, 'w') as plaintext_handle:
                plaintext_handle.write(yaml.safe_dump({  # type: ignore
                    'secrets': {
                        'test_user': 'Einstein',
                        'test_password': 'E=m*C^2',
                    },
                }))
        logger.info('  Done!')

    encrypt(subs)
    return True
