import argparse


def parser_builder():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--auth',
        required=True,
        help='JSON authentication file',
        type=argparse.FileType('r'))
    parser.add_argument(
        '-p',
        '--projects',
        required=True,
        help='JSON of projects set',
        type=argparse.FileType('r'))
    return parser


def parse_args(cli_parser=parser_builder()):
    cli_parser.parse_args()
