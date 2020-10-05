# Standard library
import io
import json
import pytest
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)

# Local libraries
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


def test_cli_integration():
    args = f"--project fluidattacks/product --max-pages 2"

    out_buffer, err_buffer = io.StringIO(), io.StringIO()

    with redirect_stdout(out_buffer), redirect_stderr(err_buffer):
        cli.parse_args(args.split())
    lines = out_buffer.getvalue().splitlines()
    assert len(lines) == 400
    for line in lines:
        obj = json.loads(line)
        assert 'stream' in obj
        assert obj['stream'] in ('jobs', 'merge_requests')
        assert 'record' in obj
        assert 'id' in obj['record']
        if obj['stream'] == 'jobs':
            assert 'commit' in obj['record']
        if obj['stream'] == 'merge_requests':
            assert 'merge_commit_sha' in obj['record']
