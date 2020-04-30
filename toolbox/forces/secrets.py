# Standard library
import glob
import os

# Third party imports
import ruamel.yaml as yaml

# Local imports
from toolbox import (
    logger,
    utils,
)


def encrypt(subs: str) -> bool:
    """Encrypt a secrets.yml file for a group."""
    # pylint: disable=import-outside-toplevel
    from fluidasserts.helper import crypto

    utils.generic.aws_login(f'continuous-{subs}')

    for resources in glob.glob(f'groups/{subs}/forces/*/resources'):
        plaintext: str = f'{resources}/plaintext.yml'
        secrets: str = f'{resources}/secrets.yml'

        logger.info(f'Moving secrets from {plaintext} to {secrets}')

        with open(plaintext) as plaintext_handle, \
                open(secrets, 'w') as encrypted_handle:
            crypto.create_encrypted_yaml(
                key_b64=utils.generic.get_sops_secret(
                    f'forces_aws_secret_access_key',
                    f'groups/{subs}/config/secrets.yaml',
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
    """Decrypt a secrets.yml file for a group."""
    # pylint: disable=import-outside-toplevel
    from fluidasserts.helper import crypto

    utils.generic.aws_login(f'continuous-{subs}')

    for resources in glob.glob(f'groups/{subs}/forces/*/resources'):
        plaintext: str = f'{resources}/plaintext.yml'
        secrets: str = f'{resources}/secrets.yml'

        if not os.path.exists(secrets):
            logger.info(f'Initializing {plaintext} because it did not exist')
            with open(plaintext, 'w') as plaintext_handle:
                plaintext_handle.write(yaml.safe_dump({  # type: ignore
                    'secrets': {
                        'test_user': 'Einstein',
                        'test_password': 'E=m*C^2',
                    },
                }))
        else:
            logger.info(f'Moving secrets from {secrets} to {plaintext}')

            crypto.create_decrypted_yaml(
                key_b64=utils.generic.get_sops_secret(
                    f'forces_aws_secret_access_key',
                    f'groups/{subs}/config/secrets.yaml',
                    f'continuous-{subs}'),
                input_file=secrets,
                output_file=plaintext)

        logger.info('  Done!')

    encrypt(subs)
    return True
