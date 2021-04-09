# Standard library
import argparse

# Third party libraries
from ruamel.yaml import (
    safe_dump,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    for arg in ('check', 'group', 'language', 'namespace', 'out'):
        parser.add_argument(f'--{arg}', required=True)
    args = parser.parse_args()

    data: str = safe_dump(
        dict(
            checks=[
                args.check,
            ],
            language=args.language,
            namespace=args.namespace,
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
    main()
