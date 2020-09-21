# Standard library
import json
import os
import sys


def main() -> None:
    with open(os.path.join(os.environ['STARTDIR'], 'env.lst')) as file:
        secrets = list(filter(None, file.read().splitlines()))

    data = {
        'command': sys.argv[3:],
        'environment': [
            {'name': secret, 'value': os.environ[secret]}
            for secret in secrets
            if secret in os.environ
        ],
        'memory': int(sys.argv[2]),
        'vcpus': int(sys.argv[1]),
    }

    print(json.dumps(data, indent=2))
    data['environment'] = '...'
    print(json.dumps(data, indent=2), file=sys.stderr)


if __name__ == '__main__':
    main()
