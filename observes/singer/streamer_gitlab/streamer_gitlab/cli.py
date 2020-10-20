# Standard libraries
import sys
import argparse
from os import (
    environ,
)
from typing import List

# Third party libraries
from aioextensions import (
    run,
)

# Local libraries
from streamer_gitlab.extractor import main
from streamer_gitlab.log import log


def parser_builder():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--projects',
        required=True,
        help='Projects for analisis',
        nargs='*'
    )
    parser.add_argument(
        '--max-pages',
        type=int,
        help='Number of max pages',
        default=10000
    )
    return parser


def parse_args(args: List[str] = None):
    try:
        api_token = environ['GITLAB_API_TOKEN']
    except KeyError:
        log('critical', 'Export GITLAB_API_TOKEN as environment variable')
        sys.exit(1)
    else:
        parsed_args = parser_builder().parse_args(args)
        run(main(parsed_args.projects, api_token, parsed_args.max_pages))
