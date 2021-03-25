# Standard library
import glob
import json
import os
import re
from typing import (
    Dict,
    List,
)

# Local libraries
from model import (
    core_model,
)
from utils.encodings import (
    yaml_dumps_blocking,
)

# Constants
FOLDER = '../owasp_benchmark'


def get_tests_cases() -> Dict[str, List[str]]:
    tests = {}
    pattern = re.compile(r'@WebServlet\(value="/(\w+)-', flags=re.MULTILINE)
    test_files = sorted(glob.glob(
        f'{FOLDER}/src/main/java/org/owasp/benchmark/testcode/*.java',
    ))

    for test_file in test_files:
        with open(test_file) as handle:
            content = handle.read()

        if match := pattern.search(content):
            category = match.group(1)
            tests.setdefault(category, [])
            tests[category].append(os.path.relpath(test_file, FOLDER))
        else:
            raise Exception(content)

    return tests


def main() -> None:
    suites: List[str] = []
    categories = {
        'cmdi': [core_model.FindingEnum.F004.name],
        'pathtraver': [core_model.FindingEnum.F063_PATH_TRAVERSAL.name],
        'sqli': [core_model.FindingEnum.F001_JAVA_SQL.name],
        'securecookie': [core_model.FindingEnum.F042.name],
        'weakrand': [core_model.FindingEnum.F034.name],
        'xss': [core_model.FindingEnum.F008.name],
    }
    extra_files: List[str] = [
        'src/main/java/org/owasp/benchmark/helpers/DatabaseHelper.java'
    ]

    for category, tests_cases in get_tests_cases().items():
        tests_cases.sort()

        suite = f'benchmark_owasp_{category}'
        suites.append(suite)

        content = yaml_dumps_blocking(dict(
            namespace='OWASP',
            output=f'skims/test/outputs/{suite}.csv',
            path=dict(
                include=extra_files + tests_cases,
                lib_path=False,
                lib_root=categories.get(category, [])
            ),
            working_dir=FOLDER,
        ))

        with open(f'skims/test/data/config/{suite}.yaml', 'w') as handle:
            handle.write(content)

    print(json.dumps(suites, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
