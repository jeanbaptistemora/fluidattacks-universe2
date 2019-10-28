#!/usr/bin/env python3

from base64 import b64encode
from sys import argv
from shlex import quote
from ruamel.yaml import YAML


def sops_env_yaml(input_file):
    """
    Export environment variables from a yaml file

    :param input_file: Yaml file
    """

    yaml = YAML()
    output = 'export'

    for variable, value in yaml.load(open(input_file))['data'].items():
        value = b64encode(value.encode())
        value = quote(value.decode())
        output = f'{output} {variable}="$(echo {value} | base64 -d)"'

    print(output)


if __name__ == '__main__':
    try:
        sops_env_yaml(argv[1])
    except IndexError:
        print('Error. YAML file needed as first argument.')
        exit(1)
