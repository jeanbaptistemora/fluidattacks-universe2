# std libs
import sys
import argparse
from os import (
    environ,
)

# external libs
from aioextensions import (
    run,
)

# local libs
from streamer_gitlab.extractor import main
from streamer_gitlab.log import log


def parser_builder():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--projects',
        required=True,
        help='JSON of projects set',
        nargs='*'
    )
    return parser


def parse_args():
    try:
        api_token = environ['GITLAB_API_TOKEN']
    except KeyError:
        log('critical', 'Export GITLAB_API_TOKEN as environment variable')
        sys.exit(1)
    else:
        args = parser_builder().parse_args()
        run(main(args.projects, api_token))
