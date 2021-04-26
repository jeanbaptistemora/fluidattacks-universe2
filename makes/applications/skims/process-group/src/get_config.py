# Standard library
import argparse
import csv
from operator import (
    itemgetter,
)
import os
from typing import (
    List,
    Set,
)
from urllib.parse import (
    urlparse,
)

# Third party libraries
from aioextensions import (
    run,
)
from ruamel.yaml import (
    safe_dump,
)

# Local libraries
from integrates.dal import (
    get_group_roots,
)
from integrates.graphql import (
    create_session,
)


async def get_urls_from_group(group: str, namespace: str) -> List[str]:
    scopes: Set[str] = {
        environment_url
        for root in await get_group_roots(group=group)
        for environment_url in root.environment_urls
        if root.nickname == namespace
    }

    urls: Set[str] = set()
    urls.update(scopes)

    with open(f'groups/{group}/toe/inputs.csv') as inputs_handle:
        components = list(map(
            itemgetter('component'),
            csv.DictReader(inputs_handle),
        ))

    for scope in scopes:
        scope_c = urlparse(scope)

        for component in components:
            component_c = urlparse(f'schema://{component}')

            if (
                scope_c.netloc == component_c.netloc
                and component_c.path.startswith(scope_c.path)
            ):
                urls.add(f'{scope_c.scheme}://{component}')

    return sorted(urls)


async def main() -> None:
    parser = argparse.ArgumentParser()
    for arg in ('check', 'group', 'language', 'namespace', 'out'):
        parser.add_argument(f'--{arg}', required=True)
    args = parser.parse_args()

    create_session(os.environ['INTEGRATES_API_TOKEN'])

    data: str = safe_dump(
        dict(
            checks=[
                args.check,
            ],
            language=args.language,
            namespace=args.namespace,
            http=dict(
                include=await get_urls_from_group(args.group, args.namespace),
            ),
            path=dict(
                include=sorted([
                    "glob(*)"
                ]),
                exclude=sorted([
                    "glob(**/.git)",
                    "glob(**/*.min.js)",
                    "glob(**/*bootstrap*)",
                    "glob(**/*cordova*)",
                    "glob(**/*dynatrace*)",
                    "glob(**/*ibmmfpf.js*)",
                    "glob(**/*jquery*)",
                    "glob(**/*sjcl*)",
                    "glob(**/cryptojs/components/core.js)",
                    "glob(**/modernizr.js)",
                    "glob(**/UI/AutocompleteGenerico)",
                    "glob(**/UI/Tabs)",
                    "glob(**/.vscode)",
                    "glob(**/.idea)",
                    "glob(**/*.pydevproject)",
                    "glob(**/*.swp)",
                    "glob(**/*.launch)",
                    "glob(**/.cproject)",
                    "glob(**/.buildpath)"
                ]),
            ),
            timeout=10800,
            working_dir=f'groups/{args.group}/fusion/{args.namespace}',
        ),
        default_flow_style=False,
    )

    print(data)
    with open(args.out, 'w') as handle:
        handle.write(data)


if __name__ == '__main__':
    run(main())
