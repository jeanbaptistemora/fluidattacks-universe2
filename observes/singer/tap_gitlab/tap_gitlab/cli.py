import argparse
import logging
from os import (
    environ,
)
import sys
from typing import (
    List,
)

LOG = logging.getLogger(__name__)


def parser_builder() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--projects", required=True, help="Projects for analisis", nargs="*"
    )
    parser.add_argument(
        "--max-pages", type=int, help="Number of max pages", default=10000
    )
    return parser


def parse_args(args: List[str]) -> None:
    try:
        environ["GITLAB_ETL_API_TOKEN"]
    except KeyError:
        LOG.critical("Export GITLAB_ETL_API_TOKEN as environment variable")
        sys.exit(1)
    else:
        parser_builder().parse_args(args)
