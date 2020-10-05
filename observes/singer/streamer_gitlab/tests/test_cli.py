import json
import pytest
from streamer_gitlab import cli

def mock_data():
    return {
        'credentials_path': 'tests/mock_data/gitlab_credentials.json',
        'projects_path': 'tests/mock_data/projects.json',
    }


def test_cli_required_arguments():
    args = f""
    parser = cli.parser_builder()
    with pytest.raises(SystemExit):
        parser.parse_args(args.split())
