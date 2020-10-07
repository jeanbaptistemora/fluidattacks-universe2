# std libs
import argparse
from argparse import (
    ArgumentParser,
    Namespace,
)
# external libs

# local libs


def main_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        '--ammend-authors',
        help='Projects for analisis',
        action='store_true',
    )
    parser.add_argument(
        '--compute-bills',
        help='Projects for analisis',
        action='store_true',
    )
    parser.add_argument(
        '--upload',
        help='Projects for analisis',
        action='store_true',
    )
    return parser


def ammend_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--mailmap-path', required=True)
    return parser


def bills_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--folder', required=True)
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--month', type=int, required=True)
    return parser


def upload_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--namespace', required=True)
    parser.add_argument('repositories', nargs='*')
    return parser


def specific_parser(arg: Namespace) -> ArgumentParser:
    if arg.ammend_authors:
        return ammend_parser()
    if arg.compute_bills:
        return bills_parser()
    if arg.upload:
        return upload_parser()
    raise argparse.ArgumentTypeError('Invalid argument see help')


def specific_action(  # pylint: disable=unused-argument
    m_arg: Namespace, s_args: Namespace
) -> None:
    pass


def entrypoint():
    m_parser = main_parser()
    m_args, leftover = m_parser.parse_known_args()
    s_parser = specific_parser(m_args)
    s_args = s_parser.parse_args(leftover)
    specific_action(m_args, s_args)
