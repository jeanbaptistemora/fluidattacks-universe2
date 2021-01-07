# Standard library
import glob
import json
import os
import re
from typing import (
    Dict,
    List,
)

# Third party libraries
from more_itertools import (
    chunked,
)

# Local libraries
from utils.encodings import (
    yaml_dumps_blocking,
)

# Constants
FOLDER = '../../owasp_benchmark/src/main/java/org/owasp/benchmark/testcode'


def get_tests_cases() -> Dict[str, List[str]]:
    tests = {}
    pattern = re.compile(r'@WebServlet\(value="/(\w+)-', flags=re.MULTILINE)
    test_files = sorted(glob.glob(f'{FOLDER}/*.java'))

    for test_file in test_files:
        with open(test_file) as handle:
            content = handle.read()

        if match := pattern.search(content):
            category = match.group(1)
            tests.setdefault(category, [])
            tests[category].append(os.path.basename(test_file))
        else:
            raise Exception(content)

    return tests


def main() -> None:
    suites: List[str] = []
    for category, tests_cases in get_tests_cases().items():
        tests_cases.sort()

        for index, batch in enumerate(chunked(tests_cases, n=10)):
            suite = f'benchmark_owasp_{category}_{index}'
            suites.append(suite)

            content = yaml_dumps_blocking(dict(
                namespace=f'OWASP',
                output=f'test/outputs/{suite}.csv',
                path=dict(include=batch),
                working_dir=FOLDER,
            ))

            with open(f'test/data/config/{suite}.yaml', 'w') as handle:
                handle.write(content)

    print(json.dumps(suites, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
