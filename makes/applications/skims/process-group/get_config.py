# Standard library
import argparse
import os
from typing import (
    Set,
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


async def get_urls_from_group(group: str, namespace: str) -> Set[str]:
    return sorted({
        environment_url
        for root in await get_group_roots(group=group)
        for environment_url in root.environment_urls
        if root.nickname == namespace
    })


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
