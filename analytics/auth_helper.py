#!/usr/bin/env python3

"""Helper script to renew tokens from many providers."""

import json
import argparse
import subprocess

import urllib3

DEBUG: bool = False


def debug(*args, **kwargs) -> None:
    """Print if debugging."""
    if DEBUG:
        print(*args, **kwargs)


def run_command(cmd: str, raise_on_errors=True, raise_msg=''):
    """Run a command and return exit code, stdout and stderr."""
    debug(cmd)
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            executable='/bin/bash',
                            universal_newlines=True)
    stdout, stderr = proc.communicate()
    debug(stdout, stderr)
    if raise_on_errors and proc.returncode:
        raise Exception(f'CRITICAL: A command failed to run: {raise_msg}')
    return proc.returncode, stdout, stderr


def get_from_vault(key: str) -> str:
    """Get a key from vault."""
    _, stdout, _ = run_command(
        f'vault read -field={key} secret/serves',
        raise_on_errors=True,
        raise_msg=f'unable to get {key} from vault')
    return stdout


def get_from_url(method: str, resource: str, **kwargs) -> tuple:
    """Return the contents of a url."""
    debug(method, resource)

    with urllib3.PoolManager() as manager:
        resp = manager.request(method, resource, **kwargs)

    status, response = resp.status, None
    if 200 <= status <= 299:
        debug(status, resp.data.decode())
        response = resp.data.decode()
    else:
        debug(status, resp.data)
        raise Exception('ERROR: Unable to get resource.')
    return status, response


def timedoctor_initial_url_1(client_id, redirect_uri) -> str:
    """Return the authentication endpoint."""
    return (f'https://webapi.timedoctor.com/oauth/v2/auth'
            f'?client_id={client_id}'
            f'&redirect_uri={redirect_uri}'
            f'&response_type=code')


def timedoctor_initial_url_2(
        code, client_id, client_secret, redirect_uri) -> str:
    """Return the authentication endpoint."""
    return (f'https://webapi.timedoctor.com/oauth/v2/token'
            f'?code={code}'
            f'&client_id={client_id}'
            f'&client_secret={client_secret}'
            f'&redirect_uri={redirect_uri}'
            f'&grant_type=authorization_code')


def timedoctor_refresh_url(
        client_id: str, client_secret: str, refresh_token: str) -> str:
    """Return the refresh url for timedoctor."""
    return (f'https://webapi.timedoctor.com/oauth/v2/token'
            f'?client_id={client_id}'
            f'&client_secret={client_secret}'
            f'&refresh_token={refresh_token}'
            f'&grant_type=refresh_token')


def timedoctor_start() -> bool:
    """Scrip to refresh the timedoctor token."""
    timedoctor = json.loads(get_from_vault('analytics_auth_timedoctor'))

    print(timedoctor_initial_url_1(
        client_id=timedoctor['client_id'],
        redirect_uri=timedoctor['redirect_uri']))
    print()
    code = input('code: ')
    print()

    # Get the new token
    new_timedoctor = json.loads(get_from_url(
        method='GET',
        resource=timedoctor_initial_url_2(
            code=code,
            client_id=timedoctor['client_id'],
            client_secret=timedoctor['client_secret'],
            redirect_uri=timedoctor['redirect_uri']),
        headers={'Authorization': f'Bearer {timedoctor["access_token"]}'})[1])

    # Put it on vault, tokens are issued with 2 hours of duration
    new_values = json.dumps(
        {**timedoctor, **new_timedoctor}).replace('"', '\\"')
    run_command((f"source './infrastructure/vault-wrapper.sh';"
                 f"vault_update_variables"
                 f"  serves"
                 f"  'analytics_auth_timedoctor={new_values}'"),
                raise_on_errors=True,
                raise_msg=f'unable to update using vault-wrapper')
    return True


def timedoctor_update(json_str: str) -> bool:
    """Just put in vault this values."""
    timedoctor = json.loads(get_from_vault('analytics_auth_timedoctor'))

    # Put it on vault, tokens are issued with 2 hours of duration
    new_values = json.dumps(
        {**timedoctor, **json.loads(json_str)}).replace('"', '\\"')
    run_command((f"source './infrastructure/vault-wrapper.sh';"
                 f"vault_update_variables"
                 f"  serves"
                 f"  'analytics_auth_timedoctor={new_values}'"),
                raise_on_errors=True,
                raise_msg=f'unable to update using vault-wrapper')
    return True


def timedoctor_refresh() -> bool:
    """Scrip to refresh the timedoctor token."""
    # Get the current values
    timedoctor = json.loads(get_from_vault('analytics_auth_timedoctor'))

    # Get the new token
    new_timedoctor = json.loads(get_from_url(
        method='GET',
        resource=timedoctor_refresh_url(
            client_id=timedoctor['client_id'],
            client_secret=timedoctor['client_secret'],
            refresh_token=timedoctor['refresh_token']),
        headers={'Authorization': f'Bearer {timedoctor["access_token"]}'})[1])

    # Put it on vault, tokens are issued with 2 hours of duration
    new_values = json.dumps(
        {**timedoctor, **new_timedoctor}).replace('"', '\\"')
    run_command((f"source './infrastructure/vault-wrapper.sh';"
                 f"vault_update_variables"
                 f"  serves"
                 f"  'analytics_auth_timedoctor={new_values}'"),
                raise_on_errors=True,
                raise_msg=f'unable to update using vault-wrapper')

    return True


def main():
    """Usual entrypoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--timedoctor-start',
        action='store_true')
    parser.add_argument(
        '--timedoctor-update',
        metavar='json_str',
        required=False)
    parser.add_argument(
        '--timedoctor-refresh',
        action='store_true')
    args = parser.parse_args()

    if args.timedoctor_start:
        timedoctor_start()
    elif args.timedoctor_update:
        timedoctor_update(args.timedoctor_update)
    elif args.timedoctor_refresh:
        timedoctor_refresh()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
