import json
import pytest
from tap_gitlab import cli

def mock_data():
    return {
        'credentials_path': 'tests/mock_data/gitlab_credentials.json',
        'projects_path': 'tests/mock_data/projects.json',
    }

def test_cli_arguments_support():
    data = mock_data()
    args = f"--auth {data['credentials_path']} --projects {data['projects_path']}"
    parser = cli.parser_builder()
    parser.parse_args(args.split())

def test_cli_required_arguments():
    data = mock_data()
    args = f"--projects {data['projects_path']}"
    parser = cli.parser_builder()
    with pytest.raises(SystemExit):
        parser.parse_args(args.split())